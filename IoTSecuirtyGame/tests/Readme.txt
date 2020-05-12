Preparation for running the tests:
1. Install python3 and set it into the system path
2. pip install selenium
3. download geckodriver and chromedriver, add their paths to the system path
4. run server in local:
    >cd to_your_server_dir
    >python server.py 8080 nocheck noswitch

    after the server run, open the browser, go to instructor dashboard url:
    http://localhost:8080/instructor-dashboard.html#!/?cheat
    Select not load the previous state by click No button

For the testing result:
1. install the report tools,: refer to:  https://www.dev2qa.com/python-3-unittest-html-and-xml-report-example/
If use html file for reporting
    > pip install html-testRunner
2. In your test scripts:
  import HtmlTestRunner
3. In your test scripts, pass the testRunner object to the unittest.main, and specify the output file directory
  for example:
  if __name__ == '__main__':
    unittest.main(verbosity=2,
                  testRunner=HtmlTestRunner.HTMLTestRunner(output=r'C:\Users\sammi\OneDrive\Desktop\iot-test-results'))

About the Scripts:
1. The scripts are written in unittest framework. How to use unittest? Please check 
    https://docs.python.org/3/library/unittest.html#

