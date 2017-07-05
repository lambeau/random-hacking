// http://www.mtgsalvation.com/spoilers/183-hour-of-devastation

cards = {}
$('.t-spoiler-container').each(function(k,v) {
  // Name and cost
  info = $(v).find('.t-spoiler-header')[0].innerText.split('\n')
  name = info[0]
  cost = info[1]
  // Number
  number = parseInt($(v).find('.t-spoiler-artist')[0].innerText.split('#')[1].trim().split('/')[0])
  // Type
  type = $(v).find('.t-spoiler-type')[0].innerText
  // Text
  text = $(v).find('.t-spoiler-ability')[0]
  text = text ? text.innerText.split('\n').filter(n => n) : []
  cards[number] = {'name': name, 'cost': cost, 'type': type, 'text': text}
})
console.log(JSON.stringify(cards, null, ' '))

