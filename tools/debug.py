def write_html(html):
    print('⚒️ Debug')
    print('💾 Сохранение страницы в файл')
    # Write HTML String to file.html
    with open("tools/pages/debug.html", "w") as file:
        file.write(str(html))