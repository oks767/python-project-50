from gendiff import generate_diff

diff = generate_diff('./json/file1.json', './json/file2.json')
print(diff)