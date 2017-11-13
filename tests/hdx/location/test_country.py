# -*- coding: UTF-8 -*-
"""location Tests"""
import pytest

from hdx.utilities.loader import load_json, load_file_to_str
from hdx.location.country import Country, CountryError
from hdx.utilities.path import script_dir_plus_file


class LocationError(Exception):
    pass


class TestCountry:
    def test_get_country_name_from_iso3(self):
        assert Country.get_country_name_from_iso3('jpn', use_live=False) == 'Japan'
        assert Country.get_country_name_from_iso3('awe', use_live=False) is None
        assert Country.get_country_name_from_iso3('Pol', use_live=False) == 'Poland'
        assert Country.get_country_name_from_iso3('SGP', use_live=False) == 'Singapore'
        assert Country.get_country_name_from_iso3('uy', use_live=False) is None
        with pytest.raises(LocationError):
            Country.get_country_name_from_iso3('uy', use_live=False, exception=LocationError)
        assert Country.get_country_name_from_iso3('uy', use_live=False) is None
        assert Country.get_country_name_from_iso3('VeN', use_live=False) == 'Venezuela (Bolivarian Republic of)'

    def test_get_country_info_from_iso2(self):
        assert Country.get_country_info_from_iso2('jp', use_live=False) == {'Sub-region Name': 'Eastern Asia', 'M49 Code': '392', 'ISO-alpha3 Code': 'JPN', 'Developed / Developing Countries': 'Developed', 'Land Locked Developing Countries (LLDC)': '', 'Global Name': 'World', 'Region Name': 'Asia', 'Least Developed Countries (LDC)': '', 'Intermediate Region Code': '', 'Region Code': '142', 'Country or Area': 'Japan', 'Sub-region Code': '030', 'Intermediate Region Name': '', 'Small Island Developing States (SIDS)': '', 'Global Code': '001'}
        assert Country.get_country_info_from_iso2('ab', use_live=False) is None
        with pytest.raises(LocationError):
            Country.get_country_info_from_iso2('ab', use_live=False, exception=LocationError)

    def test_get_country_name_from_iso2(self):
        assert Country.get_country_name_from_iso2('jp', use_live=False) == 'Japan'
        assert Country.get_country_name_from_iso2('ab', use_live=False) is None
        assert Country.get_country_name_from_iso2('Pl', use_live=False) == 'Poland'
        assert Country.get_country_name_from_iso2('SG', use_live=False) == 'Singapore'
        assert Country.get_country_name_from_iso2('SGP', use_live=False) is None
        with pytest.raises(LocationError):
            Country.get_country_name_from_iso2('SGP', use_live=False, exception=LocationError)
        assert Country.get_country_name_from_iso2('VE', use_live=False) == 'Venezuela (Bolivarian Republic of)'

    def test_expand_countryname_abbrevs(self):
        assert Country.expand_countryname_abbrevs('jpn') == ['JPN']
        assert Country.expand_countryname_abbrevs('Haha Dem. Fed. Republic') == ['HAHA DEMOCRATIC FED. REPUBLIC',
                                                                             'HAHA DEMOCRATIC FEDERATION REPUBLIC',
                                                                             'HAHA DEMOCRATIC FEDERAL REPUBLIC',
                                                                             'HAHA DEMOCRATIC FEDERATED REPUBLIC']

    def test_simplify_countryname(self):
        assert Country.simplify_countryname('jpn') == ('JPN', list())
        assert Country.simplify_countryname('United Rep. of Tanzania') == ('TANZANIA', ['UNITED', 'REP', 'OF'])
        assert Country.simplify_countryname('Micronesia (Federated States of)') == ('MICRONESIA', ['FEDERATED', 'STATES', 'OF'])
        assert Country.simplify_countryname('Dem. Rep. of the Congo') == ('CONGO', ['DEM', 'REP', 'OF', 'THE'])
        assert Country.simplify_countryname("Korea, Democratic People's Republic of") == ('KOREA', ['DEMOCRATIC', "PEOPLE'S", 'REPUBLIC', 'OF'])
        assert Country.simplify_countryname("Democratic People's Republic of Korea") == ('KOREA', ['DEMOCRATIC', "PEOPLE'S", 'REPUBLIC', 'OF'])
        assert Country.simplify_countryname('The former Yugoslav Republic of Macedonia') == ('MACEDONIA', ['THE', 'FORMER', 'YUGOSLAV', 'REPUBLIC', 'OF'])

    def test_get_iso3_country_code(self):
        assert Country.get_iso3_country_code('jpn', use_live=False) == 'JPN'
        assert Country.get_iso3_country_code('Dem. Rep. of the Congo', use_live=False) == 'COD'
        assert Country.get_iso3_country_code('Russian Fed.', use_live=False) == 'RUS'
        assert Country.get_iso3_country_code('Micronesia (Federated States of)', use_live=False) == 'FSM'
        assert Country.get_iso3_country_code('Iran (Islamic Rep. of)', use_live=False) == 'IRN'
        assert Country.get_iso3_country_code('United Rep. of Tanzania', use_live=False) == 'TZA'
        assert Country.get_iso3_country_code('Syrian Arab Rep.', use_live=False) == 'SYR'
        assert Country.get_iso3_country_code('Central African Rep.', use_live=False) == 'CAF'
        assert Country.get_iso3_country_code('Rep. of Korea', use_live=False) == 'KOR'
        assert Country.get_iso3_country_code('St. Pierre and Miquelon', use_live=False) == 'SPM'
        assert Country.get_iso3_country_code('Christmas Isl.', use_live=False) == 'CXR'
        assert Country.get_iso3_country_code('Cayman Isl.', use_live=False) == 'CYM'
        assert Country.get_iso3_country_code('jp', use_live=False) == 'JPN'
        assert Country.get_iso3_country_code_fuzzy('jpn', use_live=False) == ('JPN', True)
        assert Country.get_iso3_country_code_fuzzy('ZWE', use_live=False) == ('ZWE', True)
        assert Country.get_iso3_country_code_fuzzy('Vut', use_live=False) == ('VUT', True)
        assert Country.get_iso3_country_code('abc', use_live=False) is None
        with pytest.raises(LocationError):
            Country.get_iso3_country_code('abc', use_live=False, exception=LocationError)
        assert Country.get_iso3_country_code_fuzzy('abc', use_live=False) == (None, False)
        with pytest.raises(LocationError):
            Country.get_iso3_country_code_fuzzy('abc', use_live=False, exception=LocationError)
        assert Country.get_iso3_country_code_fuzzy('United Kingdom', use_live=False) == ('GBR', False)
        assert Country.get_iso3_country_code_fuzzy('United Kingdom of Great Britain and Northern Ireland', use_live=False) == ('GBR', True)
        assert Country.get_iso3_country_code_fuzzy('united states', use_live=False) == ('USA', False)
        assert Country.get_iso3_country_code_fuzzy('united states of america', use_live=False) == ('USA', True)
        assert Country.get_iso3_country_code('UZBEKISTAN', use_live=False) == 'UZB'
        assert Country.get_iso3_country_code_fuzzy('UZBEKISTAN', use_live=False) == ('UZB', True)
        assert Country.get_iso3_country_code('Sierra', use_live=False) is None
        assert Country.get_iso3_country_code_fuzzy('Sierra', use_live=False) == ('SLE', False)
        assert Country.get_iso3_country_code('Venezuela', use_live=False) is None
        assert Country.get_iso3_country_code_fuzzy('Venezuela', use_live=False) == ('VEN', False)
        assert Country.get_iso3_country_code_fuzzy('Heard Isl.', use_live=False) == ('HMD', False)
        assert Country.get_iso3_country_code_fuzzy('Falkland Isl.', use_live=False) == ('FLK', False)
        assert Country.get_iso3_country_code_fuzzy('Czech Republic', use_live=False) == ('CZE', False)
        assert Country.get_iso3_country_code_fuzzy('Czech Rep.', use_live=False) == ('CZE', False)
        assert Country.get_iso3_country_code_fuzzy('Islamic Rep. of Iran', use_live=False) == ('IRN', False)
        assert Country.get_iso3_country_code_fuzzy('Dem. Congo', use_live=False) == ('COD', False)
        assert Country.get_iso3_country_code_fuzzy('Congo, Republic of', use_live=False) == ('COG', False)
        assert Country.get_iso3_country_code_fuzzy('Republic of the Congo', use_live=False) == ('COG', False)
        assert Country.get_iso3_country_code_fuzzy('Vietnam', use_live=False) == ('VNM', False)
        assert Country.get_iso3_country_code_fuzzy('South Korea', use_live=False) == ('KOR', False)
        assert Country.get_iso3_country_code_fuzzy('Korea Republic', use_live=False) == ('KOR', False)
        assert Country.get_iso3_country_code_fuzzy('Dem. Republic Korea', use_live=False) == ('PRK', False)
        assert Country.get_iso3_country_code_fuzzy('North Korea', use_live=False) == ('PRK', False)
        assert Country.get_iso3_country_code_fuzzy('Serbia and Kosovo: S/RES/1244 (1999)', use_live=False) == ('SRB', False)
        assert Country.get_iso3_country_code_fuzzy('U.S. Virgin Islands', use_live=False) == ('VIR', True)
        assert Country.get_iso3_country_code_fuzzy('U.K. Virgin Islands', use_live=False) == ('VGB', False)
        with pytest.raises(ValueError):
            Country.get_iso3_country_code('abc', use_live=False, exception=ValueError)
        with pytest.raises(ValueError):
            Country.get_iso3_country_code_fuzzy('abc', use_live=False, exception=ValueError)

    def test_get_countries_in_region(self):
        assert len(Country.get_countries_in_region('Africa', use_live=False)) == 60
        assert Country.get_countries_in_region('013', use_live=False) == ['BLZ', 'CRI', 'GTM', 'HND', 'MEX', 'NIC', 'PAN', 'SLV']
        assert Country.get_countries_in_region('Channel Islands', use_live=False) == ['GGY', 'JEY']
        assert len(Country.get_countries_in_region('NOTEXIST', use_live=False)) == 0
        with pytest.raises(LocationError):
            Country.get_countries_in_region('NOTEXIST', use_live=False, exception=LocationError)

    def test_wb_feed_file_working(self):
        json = load_json(script_dir_plus_file('worldbank.json', TestCountry))
        html = load_file_to_str(script_dir_plus_file('unstats.html', TestCountry))
        Country.set_countriesdata(json, html, dict())
        assert Country.get_iso3_country_code('UZBEKISTAN', use_live=False) is None
        assert Country.get_iso3_country_code('south sudan', use_live=False) == 'SSD'
        html = load_file_to_str(script_dir_plus_file('unstats_emptytable.html', TestCountry))
        with pytest.raises(CountryError):
            Country.set_countriesdata(json, html, dict())
        Country.set_worldbank_url()
        Country.set_unstats_url_tablename('NOTEXIST')
        Country._countriesdata = None
        assert Country.get_iso3_country_code('UZBEKISTAN', use_live=True) == 'UZB'
        Country.set_unstats_url_tablename()
        Country.set_worldbank_url('NOTEXIST')
        Country._countriesdata = None
        assert Country.get_iso3_from_iso2('AF') == 'AFG'
        Country.set_unstats_url_tablename(tablename='NOTEXIST')
        Country.set_worldbank_url()
        Country._countriesdata = None
        with pytest.raises(CountryError):
            Country.get_countries_in_region('Caribbean')
        Country.set_unstats_url_tablename()
        Country._countriesdata = None
        assert len(Country.get_countries_in_region('Africa')) == 60