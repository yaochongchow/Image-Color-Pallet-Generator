import numpy as np
from PIL import Image, ImageDraw, ImageFont
from sklearn.cluster import MiniBatchKMeans

def create_bar(height, width, color):
    bar = np.zeros((height, width, 3), np.uint8)
    bar[:, :] = color
    return bar

def generate_color_palette(image_path, num_colors):
    # Open the image
    image = Image.open(image_path)

    # Convert image to numpy array
    image_array = np.array(image)

    # Flatten the image array
    pixels = image_array.reshape(-1, 3)

    # Perform Mini-Batch K-means clustering
    kmeans = MiniBatchKMeans(n_clusters=num_colors, batch_size=1000)
    kmeans.fit(pixels)

    # Get the RGB values of the cluster centers
    colors = kmeans.cluster_centers_.astype(int)

    return colors

def save_color_palette(color_palette, save_path):
    num_colors = color_palette.shape[0]
    bar_width = 200
    bar_height = 100

    # Create a new image with the color palette
    palette_width = bar_width
    palette_height = num_colors * bar_height
    palette_image = Image.new('RGB', (palette_width, palette_height), (255, 255, 255))

    # Draw hex code on each color palette
    draw = ImageDraw.Draw(palette_image)
    font = ImageFont.truetype('Fonts/Poppins-Black.ttf', 14)

    for i in range(num_colors):
        color = tuple(color_palette[i])
        bar = create_bar(bar_height, bar_width, color)
        palette_image.paste(Image.fromarray(bar), (0, i * bar_height))

        # Convert RGB to hex code
        hex_code = '#%02x%02x%02x' % color

        # Calculate text position for center alignment
        text_x = (bar_width - font.getbbox(hex_code)[2]) // 2
        text_y = (bar_height - font.getbbox(hex_code)[3]) // 2 + i * bar_height

        # Draw hex code on color palette
        draw.text((text_x, text_y), hex_code, font=font, fill='black')

    # Save the color palette as a PNG image with high quality
    palette_image.save(save_path, dpi=(300, 300))

# Example usage
image_path = 'Images/Input Images/th.jpg'
save_path = 'Images/Palettes/palette.png'

# Asking user for the number of color palettes
num_colors = int(input("Enter how many color palettes you want: "))

# Generate the color palette
color_palette = generate_color_palette(image_path, num_colors)

# Save the color palette as a PNG image with high quality
save_color_palette(color_palette, save_path)
