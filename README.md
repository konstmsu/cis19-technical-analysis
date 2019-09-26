# Technical Analysis

Build trading strategy to maximize profit based on the past behaviour of a stock price.

See [Insturctions notebook](instructions.ipynb) for details.

Developed by Konstantin Spirin for CodeIT Suisse 2019.

TODO:

- Disabled solver should not return 405
- Mention alternating buy-sell in assumptions rather than output
- Scale displayed maths (via cookies?)
- Test in both HK and SG
- Create evaluator notebook
- Script to clone all repos from heroku?
- How to avoid committing generated zip and html but still have them on Heroku?
- ✓ (maybe) Disable sample solver in production via feature toggle
- ✓ Use pprint for sample data
- ✓ Add Favicon
- ✓ Align code and markdown in instructions.html
- ✓ Log ~~model parameters~~ random seed
- ✓ Refactor to consolidate usage of test_client
- ✗ ~~Mention model parameters in instructions and add to inspiration visualization titles~~
- ✓ Move sample input to "input section" in instructions page
- ✓ Think about how to reformulate "full index range"
- ✓ Add axis labels on the first illustration
- ✓ Add code snippet to generate more training data
- ✓ Publish to EU
- ✓ Add "Challenge" to instructions page title
- ✓ Add .txt extension to readme in sample_data.zip to be able to open on Windows
- ✓ Add solution running time to message
- ✓ Check sample_data.zip can be opened on Windows and contains README
- ✓ Handle timeouts
- ✓ Increase complexity to 10
- ✓ Add instructions page link to confluence
- ✓ Add link to zip into instructions
- ✓ Generate more training data
- ✓ ! First image is not rendered on instructions page
- ✓ Include content into non-200 errors
- ✓ Instructions page title should mention "Technical Analysis"
- ✓ Problem visualization at the beginning?
- ✓ CPU resources for solvers - they host wherever they want
- ✓ Hide code on instructions page
- ✓ Add timeout information on instructions page
- ✓ Document that score_i is never less than 0
- ✓ Document "ceil" in scoring in instructions
- ✓ Add smaller sample to the instructions page
- ✓ Check solution return code and return 0 to cooridnator on exception
- ✓ Fix failing production test submission
- ✓ Check max message size and exclude optimal trades
- ✓ What does evaluate callback return? (see logs) - empty body
