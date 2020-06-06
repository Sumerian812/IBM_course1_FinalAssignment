import bs4
import requests
import pandas as pd


def get_basketball_stats(url='https://en.wikipedia.org/wiki/Michael_Jordan'):
    # read the web page
    response = requests.get(url)
    # create a BeautifulSoup object to parse the HTML
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    # the player stats are defined  with the attribute CSS class set to 'wikitable sortable';
    # therefore we create a tag object "table"
    table = soup.find(class_='wikitable sortable')

    # the headers of the table are the first table row (tr) we create a tag object that has the first row
    headers = table.tr

    # the table column names are displayed  as an abbreviation; therefore we find all the abbr tags and returns an
    # Iterator
    titles = headers.find_all("abbr")  # list
    # we create a dictionary  and pass the table headers as the keys
    data = {title['title']: [] for title in titles}
    # we will store each column as a list in a dictionary, the header of the column will be the dictionary key

    # we iterate over each table row by fining each table tag tr and assign it to the object
    for row in table.find_all('tr')[1:]:

        # we iterate over each cell in the table, as each cell corresponds to a different column we all obtain the
        # corresponding key corresponding the column n
        for key, a in zip(data.keys(), row.find_all("td")[2:]):
            # we append each element and strip any extra HTML content
            data[key].append(''.join(c for c in a.text if (c.isdigit() or c == ".")))

    # we remove extra rows by finding the smallest list
    Min = min([len(x) for x in data.values()])
    # we convert the elements in the key to floats
    for key in data.keys():
        data[key] = list(map(lambda x: float(x), data[key][:Min]))
    return data


links = ['https://en.wikipedia.org/wiki/Michael_Jordan', 'https://en.wikipedia.org/wiki/Kobe_Bryant',
         'https://en.wikipedia.org/wiki/LeBron_James', 'https://en.wikipedia.org/wiki/Stephen_Curry']
names = ['Michael Jordan', 'Kobe Bryant', 'Lebron James', 'Stephen Curry']


for index, link in enumerate(links):
    df = pd.DataFrame(get_basketball_stats(link))
    print(str(names[index]) + "\n" + str(df.head()))
    csv_name = str(names[index].replace(" ", "")) + '.csv'
    df.to_csv(csv_name)



