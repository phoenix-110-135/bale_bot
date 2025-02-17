<!DOCTYPE html>
<html lang="fa">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">

</head>
<body>

<h1>README for Telegram Bot</h1>

<h2>Overview</h2>
<p>This is a simple Telegram bot built using the Bale framework that allows users to play a guessing game, earn coins, and generate discount codes. The bot interacts with users through inline buttons and stores user data in SQLite databases.</p>

<h2>Features</h2>
<ul>
  <li><strong>User Registration</strong>: New users are added to the database upon starting the bot.</li>
  <li><strong>Guessing Game</strong>: Users can play a number guessing game where they guess a number between 0 and 100.</li>
  <li><strong>Coin System</strong>: Users earn coins by winning games and can use them to generate discount codes.</li>
  <li><strong>Discount Code Generation</strong>: Users can redeem coins for discount codes.</li>
</ul>

<h2>Requirements</h2>
<ul>
  <li>Python 3.7 or higher</li>
  <li>Bale library</li>
  <li>SQLite3</li>
  <li>Additional libraries: <code>random</code>, <code>string</code>, <code>json</code></li>
</ul>

<h2>Installation</h2>
<pre><code>git clone &lt;repository_url&gt;
cd &lt;repository_directory&gt;</code></pre>
<pre><code>pip install bale</code></pre>
<p>Create the SQLite databases:</p>
<ul>
  <li><code>UserInfo.db</code> for storing user information.</li>
  <li><code>GiftCode.db</code> for storing generated discount codes.</li>
</ul>

<h2>Usage</h2>
<ol>
  <li>Replace <code>your_token</code> in the bot initialization with your actual Telegram bot token.</li>
  <pre><code>bot = Bot(token="your_token")</code></pre>
  <li>Run the bot:</li>
  <pre><code>python bot.py</code></pre>
</ol>

<h2>Bot Commands</h2>
<ul>
  <li><code>/start</code>: Register the user and show the main menu with options to play the game, get a discount code, or view user account details.</li>
</ul>

<h2>Database Structure</h2>

<h3>UserInfo.db</h3>
<p><strong>Table</strong>: <code>users</code></p>
<ul>
  <li><code>id</code>: INTEGER PRIMARY KEY</li>
  <li><code>chat_id</code>: INTEGER</li>
  <li><code>name</code>: TEXT</li>
  <li><code>referrals</code>: TEXT</li>
  <li><code>total_playes</code>: INTEGER</li>
  <li><code>coin</code>: INTEGER</li>
</ul>

<h3>GiftCode.db</h3>
<p><strong>Table</strong>: <code>codes</code></p>
<ul>
  <li><code>id</code>: INTEGER PRIMARY KEY</li>
  <li><code>code_id</code>: TEXT</li>
  <li><code>user_id</code>: INTEGER</li>
</ul>

<h2>Code Summary</h2>
<ul>
  <li><strong>Database Functions</strong>:
      <ul>
          <li><code>add_user_to_db(chat_id, name)</code>: Adds a new user to the database.</li>
          <li><code>get_user_data(chat_id)</code>: Retrieves user data.</li>
          <li><code>edit_coins(chat_id)</code>: Increases the user's coin count.</li>
          <li><code>zero_coins(chat_id)</code>: Resets the user's coins to zero.</li>
          <li><code>create_GiftCode(code_id, user_id)</code>: Creates a new discount code for a user.</li>
          <li><code>gen_random_code(length=8)</code>: Generates a random alphanumeric code.</li>
      </ul>
  </li>
  <li><strong>Bot Events</strong>:
      <ul>
          <li><code>on_ready()</code>: Confirms the bot is ready.</li>
          <li><code>on_message(message: Message)</code>: Handles incoming messages and user commands.</li>
          <li><code>on_callback(callback: CallbackQuery)</code>: Handles button interactions.</li>
      </ul>
  </li>
</ul>

<h2>Contributing</h2>
<p>Feel free to fork the repository and submit pull requests for any improvements or new features.</p>

<h2>License</h2>
<p>This project is licensed under the MIT License. See the LICENSE file for details.</p>

<h3>For any questions or issues, please contact the maintainer. Happy coding!</h3>

</body>
</html>
