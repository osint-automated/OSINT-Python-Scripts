def defang(url_list):
    """
    Replaces every '.' in each URL from the input list with '[.]' and prints the modified URLs.

    Args:
        url_list (list of str): List of URLs to be defanged.

    Returns:
        None
    """
    for url in url_list:
        new_link = url.replace('.', '[.]')
        print(new_link)

if __name__ == "__main__":
    with open('urls.txt', 'r') as f:
        url_list = f.readlines()
    defang(url_list)

        
        