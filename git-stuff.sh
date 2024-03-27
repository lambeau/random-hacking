# get line counts for each author in a repo
for file in $(git ls-files); do git blame --line-porcelain $file | sed -n 's/^author //p'; done | sort | uniq -c | sort -rn
