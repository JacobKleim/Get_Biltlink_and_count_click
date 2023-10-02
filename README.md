# Count click

## Project Description
 - This program allows you to get a bitlink (short website address) and count the number of clicks on this bitlink.

## Technologies and tools
 - Python

## How to use
1. Clone this repository and go to the project folder:
   ```bash
   cd /c/project_folder # for example
   
   git clone git@github.com:JacobKleim/Get_Biltlink_and_count_click.git
   
   cd /c/project_folder/Get_Biltlink_and_count_count_click 
   ```

2. Create a .env file with parameters:
   ```
   BITLINK_TOKEN=some_token # add your token from bitlink
   ```

3. Сreate and activate a virtual environment:
   ```bash
   python -m venv venv 
   
   source venv/Scripts/activate
   ```

4. Install dependencies:
   ```bash
   python -m pip install --upgrade pip

   pip install -r requirements.txt
   ```

5. Start the project:
   ```bash
   python main.py
   ```

## Example of work
    
      
      $ python count_click.py
      Ведите ссылку: 
      $ https://www.google.com/
      Битлинк bitly.is/6Rjn5

      $ python count_click.py
      Ведите ссылку:
      $ bitly.is/6Rjn5
      По вашей ссылке прошли: 15 раз(а)
      


