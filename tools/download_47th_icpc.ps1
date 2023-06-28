$sites47 = @("xian", "hangzhou", "jinan", "hefei", "nanjing", "hongkong", "ec-final")
$sites47 | %{python .\board_downloader.py "../../local/board_data/47th/$_" 47th $_ --force}