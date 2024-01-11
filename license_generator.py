# How to sell access to my software.
# 1. Developing the software
# 2. Provide the software download
# 3. Request access information (license)
import random
import os

source = 'ABCDEFDHIJKLMNOPQRSTUVWXYZ1234567890'
generated_licenses = 0
how_many_licenses = int(input('How many licenses should be generated?'))
licenses = []

while generated_licenses <= how_many_licenses:
    license = f'{random.choices(source, k=5)}-{random.choices(source, k=5)}-{random.choices(source, k=5)}-{random.choices(source, k=5)}-{random.choices(source, k=5)}'

    clean_license = license.replace('[', '').replace("'", "").replace(',', '').replace(']', '').replace(' ', '')
    generated_licenses += 1
    licenses.append(clean_license)

    with open('licenses.txt', 'w', newline='') as file:
        file.writelines(os.linesep.join(licenses))

    print('Finished')
