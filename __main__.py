# Copyright (C) 2024  Héctor García Pérez, Airán Rivero Santana, Isaak Drija Medina, Vanja Lončarić and Bryan González Alfonso

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from PIL import Image
import re
from copy import deepcopy

# List of ASCII characters
ASCII_CHARS = [".", ",", ":", ";", "+", "*", "?", "%", "$", "#", "@"]

# Resizes the images
def resize(image, new_width=100):
    width, height = image.size
    ratio = height / width
    new_height = int(new_width * ratio)
    resized_image = image.resize((new_width, new_height))
    return resized_image

# Turns image into grayscale
def gray(image):
    grayscale_image = image.convert("L")
    return grayscale_image

# Converts each pixel into an ASCII character
def pixels_to_ascii(image):
    pixels = image.getdata()
    characters = ""
    shade_f = 255 // (len(ASCII_CHARS) - 1 ) # Calculates the color shade factor
    for pixel in pixels:
        characters += ASCII_CHARS[min(pixel // shade_f, len(ASCII_CHARS) - 1)]
    return characters   # Divides each pixel by the factor and assigns a char.

# Create the ASCII image
def create_ascii_image(new_image_data, new_image_width):
    ascii_image = ""
    for i in range(0, len(new_image_data), new_image_width):
        line = new_image_data[i:i + new_image_width]
        doubled_line = "".join([char * 2 for char in line])
        ascii_image += doubled_line + "\n"
    return ascii_image

if __name__ == "__main__":
    ASCII_CHARS_COPY = deepcopy(ASCII_CHARS) # Copies the list for inv. control
    finished = False
    while finished == False:      # Loops until user wishes to exit the program
      invert = False
      while invert == False:       # Loops until answer for inv. is valid
        inv_image = input("Do you want to invert the colors? (Yes/Y, No/N)\n")
        if inv_image.upper() not in ("YES", "Y", "NO", "N"):
          print("That is not a valid answer\n")
          continue
        if inv_image.upper() in ("YES", "Y"):        # Controls color inversion
          ASCII_CHARS = ASCII_CHARS_COPY[::-1]
          print("Color inversion enabled\n")
        else:
          print("Color inversion disabled\n")
          ASCII_CHARS = ASCII_CHARS_COPY
        invert = True

      # Ask the user to input the full pilepath to the image (no spaces supported at the moment).
      filename = str(input("Full filepath to the image (including extension): "))
      # Checks whether the input directory matches a valid Windows or UNIX directory pattern
      pattern = r"\b(.)?([\\\/])?+\.(jpg|png|webp|gif|bmp)\b" 

      # Checks if the extension is supported by the program itself.
      if re.match(pattern, filename):
        print("The file path is either not valid or the file extension is not an image.")
        continue

      if filename:                     # Checks if any files have been uploaded
        try:
            image = Image.open(filename)

            # Converts image into ASCII
            new_image_width = 100
            resized_gray_image = gray(resize(image, new_image_width))
            new_image_data = pixels_to_ascii(resized_gray_image)

            # Formats the ASCII image
            ascii_image = create_ascii_image(new_image_data, new_image_width)
            print(ascii_image)

        except:
            print("An error ocurred while opening the image.")
      else:
        print("Stopping the program...\n")
        break

      # Asks the user if he wants to continue using the program or not.
      end = input("Do you wish to upload another image? (Yes/Y, No/N)\n")
      while end.upper() not in ("YES", "Y", "NO", "N"):
        print("That is not a valid answer")
        end = input("Do you wish to upload another image? (Yes/Y, No/N)\n")
        continue
      if end.upper() in ("YES", "Y"):
        print("Restarting...\n")
        continue
      else:
        print("Stopping the program...")
        break
