import matplotlib.pyplot as plt
import base64
from io import BytesIO

# https://www.svgrepo.com/svg/187786/jupiter-planet
PARTICIPANT_ICON_SVG = """<?xml version="1.0" encoding="iso-8859-1"?>
<!-- Uploaded to: SVG Repo, www.svgrepo.com, Generator: SVG Repo Mixer Tools -->
<svg height="800px" width="800px" version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" 
	 viewBox="0 0 512 512" xml:space="preserve">
<circle style="fill:#FFAC12;" cx="255.997" cy="255.995" r="255.995"/>
<path style="fill:#D89210;" d="M256.001,0c141.383,0,255.997,114.616,255.997,255.998S397.384,511.993,256.001,511.993
	C256.001,381.73,256.001,176.014,256.001,0z"/>
<g>
	<path style="fill:#F9D026;" d="M489.914,151.847c-120.859-1.816-180.247-25.321-233.912-47.879
		C208.63,84.057,165.717,64.882,88.917,62.022c-4.766,4.114-9.421,8.426-13.944,12.95C38.16,111.785,14.92,157.024,5.218,204.479
		c70.274,16.41,157.675,78.401,250.548,85.056c0.079,0.006,0.159,0.009,0.238,0.014c83.363,5.863,171.123-46.303,254.844-57.877
		C508.254,204.344,501.267,177.36,489.914,151.847z"/>
	<path style="fill:#F9D026;" d="M308.147,381.73c-18.717,0-36.016,0.981-52.145,2.659c-83.794,8.722-135.809,36.396-188.674,44.629
		c2.484,2.705,5.021,5.379,7.643,8c49.99,49.99,115.511,74.984,181.031,74.982c65.515-0.002,131.029-24.996,181.016-74.982
		c4.149-4.149,8.111-8.416,11.915-12.77C427.571,406.73,383.832,381.73,308.147,381.73z"/>
</g>
<g>
	<path style="fill:#E7C224;" d="M256.002,289.549c83.363,5.863,171.123-46.303,254.844-57.877
		c-2.593-27.327-9.58-54.311-20.933-79.825c-120.859-1.816-180.247-25.321-233.912-47.879V289.549z"/>
	<path style="fill:#E7C224;" d="M256.002,384.389V512c65.515-0.002,131.029-24.996,181.016-74.982
		c4.149-4.149,8.111-8.416,11.915-12.77c-21.362-17.518-65.102-42.519-140.786-42.519C289.43,381.73,272.13,382.71,256.002,384.389z
		"/>
</g>
</svg>
"""

PARTICIPANT_ICON_URL = f"data:image/svg+xml;base64,{base64.b64encode(PARTICIPANT_ICON_SVG.encode("utf-8")).decode('utf-8')}"

def example_matplotlib_image():
	# Data
	categories = ['A', 'B', 'C', 'D']
	values = [10, 15, 7, 12]

	# Create bar chart
	plt.bar(categories, values)

	# Add labels and title
	plt.xlabel('Categories')
	plt.ylabel('Values')
	plt.title('Bar Chart Example')

	# Show the chart
	buffer = BytesIO()
	plt.savefig(buffer, format='png')
	buffer.seek(0)

	# Encode the BytesIO object to Base64
	image_base64 = base64.b64encode(buffer.read()).decode('utf-8')

	# Close the buffer
	buffer.close()

	return image_base64
