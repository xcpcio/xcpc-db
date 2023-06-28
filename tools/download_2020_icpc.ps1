$sites2020 = @("nanjing", "jinan", "shenyang", "kunming", "shanghai", "macau", "ec-final")
$sites2020 | %{python .\board_downloader.py "../../local/board_data/2020/$_" 2020 $_ --force}