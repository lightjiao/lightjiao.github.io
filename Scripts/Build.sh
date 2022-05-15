mkdir __Build/
mkdir __Build/Blogs/

cp ./Blogs/*.md ./__Build/Blogs/
cp ./Scripts/index.html ./__Build/
python ./Scripts/GenerateReadme.py > ./__Build/README.md