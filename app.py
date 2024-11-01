from flask import Flask, render_template, jsonify, request, redirect
from apscheduler.schedulers.background import BackgroundScheduler
import random
import datetime
import os
import json

app = Flask(__name__)

# List of funny quotes
quotes = [
    "Only two things are infinite, the universe and human stupidity, and I’m not sure about the former. — Albert Einstein",
    "I am so clever that sometimes I don’t understand a single word of what I am saying. — Oscar Wilde",
    "Get your facts first, then you can distort them as you please. — Mark Twain",
    "An expert is a man who has made all the mistakes which can be made in a very narrow field. — Niels Bohr",
    "Wine is constant proof that God loves us and loves to see us happy. — Benjamin Franklin",
    "By all means, marry. If you get a good wife, you’ll become happy; if you get a bad one, you’ll become a philosopher. — Socrates",
    "I find television very educational. Every time someone turns it on, I go in the other room and read a book. — Groucho Marx",
    "I do not feel obliged to believe that the same God who has endowed us with sense, reason, and intellect has intended us to forgo their use. — Galileo Galilei",
    "If I have seen further, it is by standing on the shoulders of giants … and then promptly taking all the credit. — Isaac Newton",
    "Life would be tragic if it weren’t funny. — Stephen Hawking",
    "Success is stumbling from failure to failure with no loss of enthusiasm. — Winston Churchill",
    "The trouble with the world is that the stupid are cocksure and the intelligent are full of doubt. — Bertrand Russell",
    "Physics is like sex: sure, it may give some practical results, but that’s not why we do it. — Richard Feynman",
    "God is a comedian playing to an audience too afraid to laugh. — Voltaire",
    "Wise men talk because they have something to say; fools, because they have to say something. — Plato",
    "The more you know, the more you realize you don’t know. — Aristotle",
    "If you wish to make an apple pie from scratch, you must first invent the universe. — Carl Sagan",
    "Sometimes a cigar is just a cigar. — Sigmund Freud",
    "I love fools' experiments. I am always making them. — Charles Darwin",
    "All of humanity's problems stem from man's inability to sit quietly in a room alone. — Blaise Pascal"
]

# Variables to store the daily quote
daily_quote = ""

# File to store reflections
REFLECTIONS_FILE = "reflections.json"

# Load existing reflections from file
def load_reflections():
    if os.path.exists(REFLECTIONS_FILE):
        with open(REFLECTIONS_FILE, 'r') as file:
            return json.load(file)
    return {}

# Save reflections to file
def save_reflections(reflections):
    with open(REFLECTIONS_FILE, 'w') as file:
        json.dump(reflections, file)

# Load reflections at startup
reflections = load_reflections()

# Scheduler function to update the quote daily
def update_daily_quote():
    global daily_quote
    daily_quote = random.choice(quotes)
    print(f"[{datetime.datetime.now()}] Daily quote updated: {daily_quote}")

# Initialize the daily quote when the app starts
update_daily_quote()

# Initialize the background scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(update_daily_quote, 'interval', days=1)
scheduler.start()

@app.route('/')
def home():
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    reflection = reflections.get(today, "")

    # Check if search parameters are passed
    search_date = request.args.get('date')
    search_result = None
    if search_date:
        search_result = reflections.get(search_date, "No reflection found for this date.")

    return render_template('index.html',
                           quote=daily_quote,
                           reflection=reflection,
                           today=today,
                           search_result=search_result,
                           search_date=search_date)



@app.route('/api/quote', methods=['GET'])
def get_quote():
    return jsonify({"quote": daily_quote})

@app.route('/reflection', methods=['POST'])
def save_reflection():
    global reflections
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    reflections[today] = request.form['reflection']
    save_reflections(reflections)
    print(f"[{datetime.datetime.now()}] Reflection saved: {reflections[today]}")
    return redirect('/')

@app.route('/api/reflections', methods=['GET'])
def get_reflections():
    return jsonify(reflections)

@app.route('/reflection/<date>', methods=['GET'])
def get_reflection_by_date(date):
    reflection = reflections.get(date, "No reflection found for this date.")
    return jsonify({"date": date, "reflection": reflection})

@app.route('/reflection/search', methods=['GET'])
def search_reflection():
    search_date = request.args.get('date')
    search_result = reflections.get(search_date, "No reflection found for this date.")
    return render_template('index.html', quote=daily_quote, reflection="", today=datetime.datetime.now().strftime("%Y-%m-%d"), search_result=search_result, search_date=search_date)


if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5015)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
