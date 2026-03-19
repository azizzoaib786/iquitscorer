# I Quit — Scoreboard

A colorful, mobile-first scoreboard app for the "I Quit" card game with real-time updates and DynamoDB persistence.

## Features

- 🎮 **Game Management** - Create and track multiple games
- 👥 **Player Management** - Add players dynamically
- 🎯 **Round System** - Organize scoring by rounds with lock/unlock functionality
- 🏆 **Live Leaderboard** - Real-time ranking with IN/OUT status
- 📜 **Game History** - View recent games on homepage
- 🔒 **Round Locking** - Lock rounds to prevent accidental changes
- 🏁 **End Round** - Quickly end and lock rounds
- ↩️ **Undo** - Revert last action
- 🎨 **Beautiful UI** - Colorful gradients and smooth animations
- 📱 **Mobile-First** - Responsive design optimized for phones

## Tech Stack

- **Backend**: FastAPI + Python
- **Frontend**: HTMX + Tailwind CSS
- **Database**: AWS DynamoDB
- **Deployment**: Uvicorn server

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables (optional)
export AWS_REGION=eu-west-1
export GAMES_TABLE=iquit_games
export EVENTS_TABLE=iquit_events

# Run the server
uvicorn app.main:app --reload --host 127.0.0.1 --port 8001
```

## Usage

1. **Create a Game**: Set game name and target score
2. **Add Players**: Enter player names
3. **Create Rounds**: Add rounds to organize scoring
4. **Score**: Enter deltas for each player per round
5. **Track Progress**: Monitor leaderboard in real-time
6. **End Round**: Lock rounds when complete
7. **Start New Round**: Scores reset per round

## Game Rules

- Players start at 0 each round
- Add positive/negative deltas to adjust scores
- Players with total ≥ target score are marked "OUT"
- Game ends when all players reach target

## Project Structure

```
iquitscorer/
├── app/
│   ├── main.py          # FastAPI routes
│   ├── db.py            # DynamoDB operations
│   ├── logic.py         # Game logic & calculations
│   ├── templates/       # Jinja2 HTML templates
│   └── static/          # JavaScript files
└── requirements.txt     # Python dependencies
```

## Developer

💻 **Developed by Aziz Zoaib**

## License

MIT
