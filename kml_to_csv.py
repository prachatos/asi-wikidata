import bs4
import unicodecsv as csv


class XmlToCsv:

    XML_DATAFILE = 'asi-monuments2.kml'

    def process(self, soup):
        data_processed = []
        i = 0
        for placemark in soup.findAll('placemark'):
            description = str(placemark.find('description'))
            desc_soup = bs4.BeautifulSoup(description, "lxml")
            lines = desc_soup.findAll('li')
            mon = {'entry': i}
            print('Processing monument ' + str(i + 1) + '...')
            for line in lines:
                name = line.find('span', {'class': 'atr-name'}).getText()
                value = line.find('span', {'class': 'atr-value'}).getText()
                mon[name] = value
            mon['lat'] = placemark.find('latitude').getText()
            mon['long'] = placemark.find('longitude').getText()
            data_processed.append(mon)
            i = i + 1
        return data_processed

    def run(self):
        print('Reading the kml file...')
        with open(self.XML_DATAFILE, encoding="utf8") as f:
            soup = bs4.BeautifulSoup(f.read(), "lxml")
            mon_list = self.process(soup)
            keys = mon_list[0].keys()
            print('Writing to monuments.csv...')
            with open('monuments.csv', 'wb') as output_file:
                dict_writer = csv.DictWriter(output_file, keys)
                dict_writer.writeheader()
                dict_writer.writerows(mon_list)
            print('Done!')


if __name__ == '__main__':
    XmlToCsv().run()