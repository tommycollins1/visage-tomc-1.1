How to Run ViSAGE v1.1
1. Install Python 3.10+
2. Clone the repository
git clone https://github.com/TEOShea1888/visage-1.1.git
cd visage-1.1


3. Install dependencies
pip install -r requirements.txt


4. Prepare input data
Ensure the following are present in data/:
- population grid
- greenspace polygons
- quality index
- travel cost surfaces
5. Run a model example
python examples/run_quality_sensitive.py


6. View outputs
Outputs will appear in:
outputs/


7. Modify scenarios
Edit files in:
config/
scenario/


to adjust:
- quality uplift
- access changes
- behavioural parameters
- spatial assumptions
