import pandas as pd

# Step 1: Load the CSV file and extract titles
df = pd.read_csv('analysis.csv')  # Load your CSV file with video titles
titles = df['title']  # Extract the 'title' column (assuming the column is named 'title')

# with open('video_title_list.txt', 'w', encoding='utf-8') as f:
#     # Iterate through the list and write each item to the file, followed by a new line
#     titles = list(titles)
#     for title in titles:
#         f.write(str(title) + '\n')

# Step 2: Define categories and associated keywords
category_keywords = {
    "League of Legends": ["lol", "esports", "champions", "riot", "legends"],
    "Minecraft Hacks": ["minecraft", "hacks", "tricks", "mods", "cheats"],
    "Clash of Clans": ["clash", "clans", "strategy", "war", "village"],
    "Game Storylines": ["storyline", "plot", "narrative", "characters", "lore"],
    "Funny Moments": ["funny", "humor", "moments", "fails", "jokes"],
    "Game Mechanics": ["mechanics", "physics", "gameplay", "systems", "controls"],
    "Game Walkthroughs": ["walkthrough", "guide", "help", "tips", "tutorial"],
    "Console Setup": ["console", "setup", "ps5", "xbox", "installation"],
    "Fortnite Tips": ["fortnite", "tips", "tricks", "guides", "battle royale"],
    "Battle Royale Updates": ["battle royale", "update", "patch", "season", "map"],
    "Game Development": ["development", "creation", "design", "coding", "dev"],
    "Esports Highlights": ["esports", "highlights", "tournament", "competition", "pro"],
    "Roblox Gameplay": ["roblox", "gameplay", "playthrough", "community", "obstacle"],
    "Mobile Game Updates": ["mobile", "game", "update", "patch", "new"],
    "Minecraft Building Tips": ["minecraft", "building", "tips", "structures", "design"],
    "Animation in Gaming": ["animation", "visuals", "graphics", "characters", "design"],
    "Brawl Stars": ["brawl stars", "brawlers", "supercell", "arena", "battle"],
    "PlayStation Guides": ["playstation", "guide", "setup", "ps4", "ps5"],
    "VR Setup": ["vr", "virtual reality", "setup", "goggles", "space"],
    "Xbox Features": ["xbox", "features", "gamepass", "series x", "controller"],
    "World of Warcraft": ["wow", "warcraft", "mmorpg", "raid", "quests"],
    "Game Trailers": ["trailer", "reveal", "teaser", "promo", "launch"],
    "Pokémon Games": ["pokemon", "catch", "trainer", "battle", "evolve"],
    "Apex Legends": ["apex", "battle royale", "legends", "characters", "shooter"],
    "FIFA Gameplay": ["fifa", "soccer", "football", "gameplay", "sports"],
    "Retro Game Reviews": ["retro", "classic", "nostalgia", "review", "old school"],
    "Horror Games": ["horror", "scary", "creepy", "survival", "thriller"],
    "Console Comparisons": ["comparison", "console", "features", "ps5", "xbox"],
    "Shooter Tutorials": ["shooter", "fps", "tips", "aiming", "combat"],
    "Animal Crossing Updates": ["animal crossing", "update", "events", "villagers", "island"],
    "Sports Games": ["sports", "game", "competition", "score", "teams"],
    "Stream Highlights": ["stream", "twitch", "highlights", "clips", "moments"],
    "Gaming Myths": ["myths", "easter eggs", "legends", "rumors", "secrets"],
    "Competitive Gaming": ["competitive", "esports", "ranked", "pro", "tournament"],
    "Easter Eggs in Games": ["easter egg", "hidden", "secret", "unlock", "bonus"],
    "Sim Games": ["simulation", "realistic", "virtual", "simulator", "model"],
    "Minecraft Survival Tips": ["minecraft", "survival", "crafting", "tips", "hardcore"],
    "League of Legends Dev Updates": ["league of legends", "dev", "update", "patch", "riot"],
    "Game Mods": ["mods", "modding", "custom", "add-on", "plugin"],
    "Assassin’s Creed": ["assassin", "creed", "ubisoft", "storyline", "history"],
    "Mobile Legends": ["mobile legends", "mlbb", "moba", "heroes", "battle"],
    "In-Game Events": ["events", "seasonal", "limited", "quests", "celebration"],
    "Super Mario Games": ["mario", "nintendo", "platformer", "classic", "levels"],
    "Minecraft Roleplay": ["minecraft", "roleplay", "story", "characters", "adventure"],
    "Racing Games": ["racing", "cars", "speed", "tracks", "vehicles"],
    "Puzzle Games": ["puzzle", "logic", "brain", "challenge", "levels"],
    "Nintendo Switch Guides": ["nintendo switch", "guide", "setup", "tips", "tricks"],
    "Realistic Graphics Games": ["graphics", "realistic", "visuals", "detail", "immersive"],
    "Game Physics": ["physics", "realism", "mechanics", "interaction", "simulation"],
    "Strategy Game Tips": ["strategy", "tips", "tactics", "planning", "gameplay"],
    "Action": ["action", "explosion", "battle", "fight", "war", "combat"],
    "Adventure": ["adventure", "journey", "explore", "quest", "mystery"],
    "RPG": ["roleplay", "rpg", "quest", "character", "level", "storyline"],
    "Strategy": ["strategy", "plan", "tactics", "gameplay", "battle", "warfare"],
    "Simulation": ["simulation", "realistic", "virtual", "model", "simulator"],
    "FPS": ["first-person", "shooter", "fps", "gun", "shooting", "battlefield"],
    "Battle Royale": ["battle royale", "survival", "fight to the death", "last man standing"],
    "Multiplayer": ["multiplayer", "online", "co-op", "team", "group"],
    "MMORPG": ["mmorpg", "mmo", "massive multiplayer", "online", "roleplay"],
    "Racing": ["racing", "race", "track", "car", "speed", "motorsport"],
    "Sports": ["sports", "football", "basketball", "soccer", "baseball", "athletics"],
    "Esports": ["esports", "competition", "tournament", "gaming championship"],
    "Indie": ["indie", "independent", "indie game", "solo", "indie developer"],
    "Horror": ["horror", "scary", "thriller", "ghost", "creepy", "horror game"],
    "MOBA": ["moba", "multiplayer online", "battle arena", "league", "heroes", "skills"],
    "Fighting": ["fighting", "combat", "beat 'em up", "brawler", "punch", "kick"],
    "Sandbox": ["sandbox", "creative", "open world", "build", "explore", "freedom"]
}

# Step 3: Function to classify titles based on keywords
def classify_title(title):
    title = title.lower()  # Convert title to lowercase to make matching case-insensitive
    for category, keywords in category_keywords.items():
        if any(keyword in title for keyword in keywords):
            return category
    return "Other"  # If no match is found, return "Other"

# Step 4: Apply classification to all titles in the dataset
df['predicted_category'] = [classify_title(title) for title in titles]

# Step 5: Save or display the results
df.to_csv('classified_video_titles.csv', index=False)  # Save the results with predicted categories
print(df[['title', 'predicted_category']].head())  # Print the first few rows to check
