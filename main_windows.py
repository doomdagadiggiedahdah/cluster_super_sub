import pygame
import time
from fractions import Fraction
import numpy as np

def get_user_input():
    while True:
        try:
            n = int(input("Enter a whole number for 'n' (greater than or equal to 1): "))
            if n >= 1:
                return n
            else:
                print("Please enter a number greater than or equal to 1.")
        except ValueError:
            print("Invalid input. Please enter a whole number.")

def generate_superparticulars(n):
    superparticulars = []
    for i in range(1, n**2 + 2*n + 1):
        superparticular = Fraction(n + i, n + i - 1)
        superparticulars.append(superparticular)
    return superparticulars

def play_frequency(frequency, duration=1000):  # Duration in milliseconds
    # Ensure pygame mixer is initialized
    if not pygame.mixer.get_init():
        pygame.mixer.init(frequency=44100, size=-16, channels=2)  # Set to stereo with channels=2
    
    # Calculate the number of frames/samples
    n_samples = int(pygame.mixer.get_init()[0] * duration / 1000.0)
    
    # Generate sound wave for mono and convert it to stereo
    mono_arr = np.array([4096 * np.sin(2.0 * np.pi * frequency * x / pygame.mixer.get_init()[0]) for x in range(n_samples)], dtype=np.int16)
    stereo_arr = np.repeat(mono_arr[:, np.newaxis], 2, axis=1)  # Duplicate the mono signal into both stereo channels
    
    # Convert the numpy array into a sound object and play it
    sound = pygame.sndarray.make_sound(stereo_arr)
    
    sound.play()
    time.sleep(duration / 1000)  # Wait for the duration to finish
    sound.stop()  # Stop the sound

def main():
    n = get_user_input()  # Get 'n' from the user
    superparticulars = generate_superparticulars(n)  # Generate superparticular ratios
    print("Generated superparticular ratios:")
    for ratio in superparticulars:
        frequency = 220 * float(ratio)  # Convert ratio to frequency based on A below middle C (220 Hz)
        print(f"Playing ratio {ratio} as frequency {frequency:.2f} Hz")
        play_frequency(frequency, 1000)  # Play each frequency for 1 second

if __name__ == "__main__":
    main()
