import pygame
import json
import random
import time
import csv
import os

# --- 1. FUNCTIONS ---

def load_config(file_path="config.json"):
    """Loads settings and trials from the JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        # Randomize trial order (optional, uncomment if needed)
        # random.shuffle(config["trials"]) 
        return config
    except FileNotFoundError:
        print(f"ERROR: Configuration file {file_path} not found.")
        return None

def save_data(data, config):
    """Saves trial data to a CSV file."""
    
    # Create the data folder
    os.makedirs("data", exist_ok=True)
    
    # Create the filename: ExpName_ParticipantID_DateTime.csv
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"data/{config['experiment_name']}_{config['participant_id']}_{timestamp}.csv"
    
    fieldnames = list(data[0].keys()) if data else []
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
        
    print(f"\nData successfully saved to: {filename}")


# --- 2. MAIN EXPERIMENT LOOP ---

def run_experiment():
    """Runs the main experiment flow."""
    
    config = load_config()
    if not config:
        return

    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode(config["screen_size"])
    pygame.display.set_caption(config["experiment_name"])
    clock = pygame.time.Clock()
    
    # Fonts
    # Using 'None' selects the default Pygame font
    font = pygame.font.Font(None, 74) 
    
    # Data collection list
    all_data = []
    
    # Create the Fixation Cross
    fixation_text = font.render("+", True, config["text_color"])
    fixation_rect = fixation_text.get_rect(center=(config["screen_size"][0] // 2, config["screen_size"][1] // 2))

    # --- EXPERIMENT START SCREEN ---
    welcome_text = font.render(f"{config['experiment_name']}. Press any key to start.", True, config["text_color"])
    screen.fill(config["background_color"])
    screen.blit(welcome_text, welcome_text.get_rect(center=(config["screen_size"][0] // 2, config["screen_size"][1] // 2)))
    pygame.display.flip()
    
    # Wait for a key press to start
    waiting_for_start = True
    while waiting_for_start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                waiting_for_start = False
                break
    
    
    # --- TRIAL LOOP ---
    for i, trial in enumerate(config["trials"]):
        
        # 1. Fixation Cross (ISI)
        screen.fill(config["background_color"])
        screen.blit(fixation_text, fixation_rect)
        pygame.display.flip()
        pygame.time.wait(config["fixation_duration_ms"])
        
        
        # 2. Stimulus Presentation
        stimulus_text = font.render(trial["stimulus"], True, config["text_color"])
        stimulus_rect = stimulus_text.get_rect(center=(config["screen_size"][0] // 2, config["screen_size"][1] // 2))
        
        screen.fill(config["background_color"])
        screen.blit(stimulus_text, stimulus_rect)
        pygame.display.flip()
        
        # Start Reaction Time Measurement
        trial_start_time = time.time() 
        response_key = "None"
        rt_ms = -999 # Default value for no response
        accuracy = 0
        responded = False
        
        # Wait for response until stimulus duration expires
        timeout_time = trial_start_time + (config["stimulus_duration_ms"] / 1000.0) 
        
        while time.time() < timeout_time and not responded:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    save_data(all_data, config) # Save data on exit
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    response_key = pygame.key.name(event.key)
                    rt_ms = round((time.time() - trial_start_time) * 1000)
                    responded = True
                    break
            
            # Regulate speed (important for display accuracy)
            clock.tick(60) 
        
        # 3. Response Evaluation and Screen Clear
        if responded:
            if response_key == trial["correct_response"]:
                accuracy = 1
            else:
                accuracy = 0
            # Response received, clear the screen immediately (for rapid trials)
            screen.fill(config["background_color"]) 
            pygame.display.flip()
            
        # If no response, clear the screen after the stimulus duration is over
        if not responded:
            screen.fill(config["background_color"])
            pygame.display.flip()
            # Wait for the remainder of the stimulus duration (to ensure fixed trial length)
            pygame.time.wait(max(0, int((timeout_time - time.time()) * 1000)))
        
        # 4. Data Logging
        trial_data = {
            "trial_num": i + 1,
            "participant_id": config["participant_id"],
            "stimulus": trial["stimulus"],
            "condition": trial["condition"],
            "correct_response": trial["correct_response"],
            "response_key": response_key,
            "RT_ms": rt_ms,
            "accuracy": accuracy
        }
        all_data.append(trial_data)
        
        # Short blank screen/Inter-Trial Interval (ITI)
        pygame.time.wait(500)

    # --- EXPERIMENT END SCREEN ---
    end_text = font.render("Experiment Complete. Thank You!", True, config["text_color"])
    screen.fill(config["background_color"])
    screen.blit(end_text, end_text.get_rect(center=(config["screen_size"][0] // 2, config["screen_size"][1] // 2)))
    pygame.display.flip()
    pygame.time.wait(3000) # Wait for 3 seconds before closing

    # --- 5. SAVE DATA AND QUIT ---
    save_data(all_data, config)
    pygame.quit()

if __name__ == "__main__":
    run_experiment()
