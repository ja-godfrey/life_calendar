#%%
import qrcode

def generate_qr_code(url):
    # Create a QR code instance
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    # Add data to the QR code
    qr.add_data(url)
    qr.make(fit=True)

    # Create an Image object from the QR code instance
    img = qr.make_image(fill='black', back_color='white')

    # Save the image to a file
    img.save("qr_code.png")

website_url = input("Enter the website URL: ")
generate_qr_code(website_url)

# %%
