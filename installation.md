
## Installation Dependencies

### Windows (see the install_dependencies.bat file to auto install)

1. Install Python 3.x from the official website.
2. Install Selenium WebDriver using the following command in the command prompt:

   ```
   py -m pip install selenium
   ```

3. Install pandas using the following command in the command prompt:

   ```
   py -m pip install pandas
   ```

4. Install requests using the following command in the command prompt:

   ```
   py -m pip install requests
   ```

5. Install BeautifulSoup using the following command in the command prompt:

   ```
   py -m pip install beautifulsoup4
   ```

6. Install Progressbar via cmd:

   ```
   py -m pip install progress progressbar2 alive-progress tqdm

   ```

7. Create a localcred.py file and define your credentials as needed.

### Linux (auto install w/ pip install -r requirements.txt)

1. Install Python 3.x using your distribution's package manager.
2. Install Selenium WebDriver using the following command in the terminal:

   ```
   pip3 install selenium
   ```

3. Install pandas using the following command in the terminal:

   ```
   pip3 install pandas
   ```

4. Install requests using the following command in the terminal:

   ```
   pip3 install requests
   ```

5. Install BeautifulSoup using the following command in the terminal:

   ```
   pip3 install beautifulsoup4
   ```

6. Install Progressbar via terminal:

   ```
   pip3 install progress progressbar2 alive-progress tqdm
   ```

7. Create a localcred.py file and define your credentials as needed.

## Credentials

Create a localcred.py file in the same directory as your script and define your credentials
<br>
** Note that this file should be kept private and not be pushed to any public repositories.
place it the .gitignore file**

## To obtain an API key for the Google Matrix API, please follow these steps:

1. **Go to the Google Cloud Console**: Visit the [Google Cloud Console](https://console.cloud.google.com/) website and log in with your Google account credentials.

2. **Create or select a project**: If you already have a project, you can skip this step. Otherwise, create a new project by clicking on the project dropdown menu at the top of the page and selecting "New Project." Give your project a meaningful name and click "Create."

3. **Enable the Google Matrix API**: In the Google Cloud Console, navigate to the project you created or selected. On the left sidebar, click on "APIs & Services" and then select "Library."

4. **Find and enable the Google Matrix API**: In the Library, search for "Google Matrix API" using the search bar. Once you find it, click on it to open the API details page. Then, click on the "Enable" button to activate the API for your project.

5. **Set up API key credentials**: After enabling the Google Matrix API, go back to the left sidebar and click on "APIs & Services," then select "Credentials."

6. **Create an API key**: On the Credentials page, click on the "Create Credentials" button and choose "API key" from the dropdown menu.

7. **Restrict your API key (optional)**: For security purposes, it's recommended to restrict your API key to specific APIs or usage limits. You can set restrictions by clicking on the "Restrict key" button and following the instructions. This step is optional but highly recommended.

8. **Copy your API key**: Once you've created your API key, a dialog box will appear displaying your API key. Copy the key to your clipboard. Note that this API key is sensitive information, so make sure to keep it secure and do not share it publicly.
