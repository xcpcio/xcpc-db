$sites46 = @('ec-final', 'macau', 'shanghai', 'nanjing', 'shenyang', 'kunming', 'jinan')
$sites46 | %{python .\board_downloader.py "../../local/board_data/46th/$_" 46th $_ --force}