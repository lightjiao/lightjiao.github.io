mkdir __Build/
rm -rf __Build/*
mkdir __Build/Blogs/

cp ./Blogs/*.md ./__Build/Blogs/
cp ./Scripts/index.html ./__Build/
python ./Scripts/GenerateReadme.py ./Blogs > ./__Build/README.md