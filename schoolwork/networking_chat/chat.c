//chat.c

//socket code taken from beej.us

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <errno.h>
#include <netdb.h>
#include <arpa/inet.h>
#include <sys/wait.h>
#include <signal.h>

#define VERSION 457
#define MESGLEN 140
#define PORT "44044"

struct Message {
	uint16_t ver;
	uint16_t len;
	unsigned char *mes;
};

void build(struct Message* message, char *mes) {
	message->ver = VERSION;
	message->len = strlen(mes);
	message->mes = (unsigned char *) mes;
}

void serialize(struct Message* mes, unsigned char *outBuf) {
	unsigned char* point = outBuf;
	uint16_t ver = htons(mes->ver);
	uint16_t len = htons(mes->len);
	memcpy(point, (unsigned char *) &ver, 2);
	memcpy(point + 2, (unsigned char *) &len, 2);
	memcpy(point + 4, mes->mes, mes->len);
}

void deserialize(struct Message* message, unsigned char *inBuf) {
	uint16_t ver;
	uint16_t len;
	unsigned char mes[141];
	unsigned char * point = inBuf;
	memcpy((unsigned char *) &ver, point, 2);
	memcpy((unsigned char *) &len, point + 2, 2);
	message->ver = ntohs(ver);
	message->len = ntohs(len);
	memcpy(mes, point + 4, message->len);
	mes[message->len] = '\0';
	message->mes = (char*) malloc((message->len + 1) * sizeof(char));
	strcpy(message->mes, mes);
//printf("%d %d %s\n",message->ver,message->len,message->mes);
}

int sendall(int s, unsigned char *buf, int *len) {
	int total = 0; // how many bytes we've sent
	int bytesleft = *len; // how many we have left to send
	int n;

	while (total < *len) {
		n = send(s, buf + total, bytesleft, 0);
		if (n == -1) {
			break;
		}
		total += n;
		bytesleft -= n;
	}

	*len = total; // return number actually sent here

	return n == -1 ? -1 : 0; // return -1 on failure, 0 on success
}

int get_message(char *input) {
	printf("You: ");
	gets(input);
	if (strlen(input) > MESGLEN) {
		printf("Error: Input too long.\n");
		return get_message(input);
	}
	return 1;
}

// get sockaddr, IPv4 or IPv6:
void *get_in_addr(struct sockaddr *sa) {
	if (sa->sa_family == AF_INET) {
		return &(((struct sockaddr_in*) sa)->sin_addr);
	}

	return &(((struct sockaddr_in6*) sa)->sin6_addr);
}

int establish_connection(char *ip, char *port, int flag) { //flag==1?server:client
	int sockfd, new_fd;
	struct addrinfo hints, *servinfo, *p;
	/**server only**/
	struct sockaddr_storage their_addr; // connector's address information
	socklen_t sin_size;
	int yes = 1;
	/**end server only**/
	char s[INET6_ADDRSTRLEN];
	int rv;

	memset(&hints, 0, sizeof hints);
	hints.ai_family = AF_UNSPEC;
	hints.ai_socktype = SOCK_STREAM;
	if (flag) {
		hints.ai_flags = AI_PASSIVE;
	}

	if ((rv = getaddrinfo(ip, port, &hints, &servinfo)) != 0) {
		fprintf(stderr, "getaddrinfo: %s\n", gai_strerror(rv));
		return -1;
	}

	// loop through all the results and connect to the first we can
	for (p = servinfo; p != NULL; p = p->ai_next) {
		if ((sockfd = socket(p->ai_family, p->ai_socktype, p->ai_protocol))
				== -1) {
			perror("socket");
			continue;
		}

		if (flag) {
			if (setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR, &yes, sizeof(int))
					== -1) {
				perror("setsockopt");
				exit(1);
			}

			if (bind(sockfd, p->ai_addr, p->ai_addrlen) == -1) {
				close(sockfd);
				perror("server: bind");
				continue;
			}
		} else {
			if (connect(sockfd, p->ai_addr, p->ai_addrlen) == -1) {
				close(sockfd);
				perror("client: connect");
				continue;
			}
		}
		break;
	}

	if (p == NULL) {
		if (flag) {
			fprintf(stderr, "server: failed to bind\n");
		} else {
			fprintf(stderr, "client: failed to connect\n");
		}
		return -1;
	}

	if (flag) {
		if (listen(sockfd, 1) == -1) {
			perror("listen");
			return -1;
		}

		//get ip address
		char *ipstr;
		char hostname[1024];
		gethostname(hostname, 1024);
		struct hostent * info;
		info = (struct hostent *) gethostbyname(hostname);
		ipstr = inet_ntoa(*((struct in_addr *) info->h_addr));
		printf("Waiting for a connection on %s port %s\n", ipstr, PORT);

		sin_size = sizeof their_addr;
		// get socket
		new_fd = accept(sockfd, (struct sockaddr *) &their_addr, &sin_size);
		if (new_fd == -1) {
			perror("accept");
		}

		inet_ntop(their_addr.ss_family,
				get_in_addr((struct sockaddr *) &their_addr), s, sizeof s);
		printf("Found a friend! You receive first.\n");

		close(sockfd); // we no longer need the listener

		sockfd = new_fd;
	} else {
		inet_ntop(p->ai_family, get_in_addr((struct sockaddr *) p->ai_addr), s,
				sizeof s);
		printf("Connecting to server... Connected!\n");
		printf("Connected to a friend! You send first.\n");
	}

	freeaddrinfo(servinfo); // all done with this structure

	return sockfd;
}

int connect_client(char *ip, char *port) {
	return establish_connection(ip, port, 0);
}

int connect_server() {
	return establish_connection(NULL, PORT, 1);
}

void client(char *ip, char *port) {
	//1. Set up a TCP connection to the server on the IP and port specified.
	int sock = connect_client(ip, port);
	if (sock == -1) {
		printf("Error: connection failed.\n");
		exit(1);
	}
	while (1) {
		unsigned char buf[MESGLEN + 5];
		//2. Prompt the user for a message to send.
		char input[1024];
		if (get_message(input)) {
			struct Message out;
			build(&out, input);
			//3. Send the message to the server.
			int len = out.len + 4;
			unsigned char outBuf[len];
			serialize(&out, outBuf);
			if (sendall(sock, outBuf, &len) == -1) {
				break;
			}
			//4. Block to receive a message from the server.
			int numbytes = recv(sock, buf, MESGLEN + 4, 0);
			if (numbytes > 0) {
				//4. Receive message and print to screen.
				struct Message in;
				deserialize(&in, buf);
				printf("Friend: %s\n", in.mes);

			} else {
				break;
			}
		}
	}
}

void server() {
	//1. Set up a TCP port and listen for connections (print out IP and PORT listening on).
	//2. Accept connection from client
	int sock = connect_server();
	if (sock == -1) {
		printf("Error: connection failed.\n");
		exit(1);
	}
	while (1) {
		unsigned char buf[MESGLEN + 5];
		int numbytes;
		//3. Block to receive a message from the client.
		numbytes = recv(sock, buf, MESGLEN + 4, 0);
		if (numbytes > 0) {
			//4. Receive message and print to screen.
			struct Message in;
			deserialize(&in, buf);
			printf("Friend: %s\n", in.mes);
			//5. Prompt the user for a message to send.
			char input[1024];
			if (get_message(input)) {
				struct Message message;
				build(&message, input);
				int len = message.len + 4;
				unsigned char outBuf[len];
				serialize(&message, outBuf);
				//6. Send the message to the client.
				if (sendall(sock, outBuf, &len) == -1) {
					break;
				}
			}
		} else {
			break;
		}
	}
}

int main(int argc, char **argv) {
	int c;
	int opt_count = 0;
	char *port = 0;
	char *ip = 0;
	while ((c = getopt(argc, argv, "s:p:")) != -1) {
		switch (c) {
		case 'p':
			port = optarg;
			opt_count++;
			break;
		case 's':
			ip = optarg;
			opt_count++;
			break;
		default:
			return 1;
		}
	}
	if (optind < argc) {
		printf("./chat: invalid parameters -- ");
		while (optind < argc)
			printf("'%s' ", argv[optind++]);
		printf("\n");
		return 1;
	}

	if (opt_count != 0 && opt_count != 2) {
		printf("Both port and server address are needed.\n");
		return 1;
	}

	if (opt_count == 0) { //then this is a server
		server();
	} else { //client
		client(ip, port);
	}
	return 0;
}
