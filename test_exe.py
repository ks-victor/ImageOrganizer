import unittest, os


class TestRenamer(unittest.TestCase):

    def test_folder1_1(self):
        file = "/Users/lallepot/Desktop/testing/test/folder1/20100717-133110.jpg"
        self.assertTrue(os.path.isfile(file))

    def test_folder1_2(self):
        file = "/Users/lallepot/Desktop/testing/test/folder1/20110916-153401.jpg"
        self.assertTrue(os.path.isfile(file))

    def test_folder1_3(self):
        file = "/Users/lallepot/Desktop/testing/test/folder1/20131028-160443.jpg"
        self.assertTrue(os.path.isfile(file))

    def test_folder1_4(self):
        file = "/Users/lallepot/Desktop/testing/test/folder1/file006004.png"
        self.assertTrue(os.path.isfile(file))

    def test_folder1_5(self):
        file = "/Users/lallepot/Desktop/testing/test/folder1/file006005.png"
        self.assertTrue(os.path.isfile(file))

    def test_folder1_count(self):
        x = len([name for name in os.listdir('/Users/lallepot/Desktop/testing/test/folder1')])
        self.assertTrue(x == 7)

    def test_folder2_1(self):
        file = "/Users/lallepot/Desktop/testing/test/folder2/20110916-153401.jpg"
        self.assertTrue(os.path.isfile(file))

    def test_folder2_2(self):
        file = "/Users/lallepot/Desktop/testing/test/folder2/20110916-153401_1.jpg"
        self.assertTrue(os.path.isfile(file))

    def test_folder2_3(self):
        file = "/Users/lallepot/Desktop/testing/test/folder2/file006000.png"
        self.assertTrue(os.path.isfile(file))

    def test_folder2_4(self):
        file = "/Users/lallepot/Desktop/testing/test/folder2/file006001.png"
        self.assertTrue(os.path.isfile(file))

    def test_folder2_5(self):
        file = "/Users/lallepot/Desktop/testing/test/folder2/file006002.png"
        self.assertTrue(os.path.isfile(file))

    def test_folder2_6(self):
        file = "/Users/lallepot/Desktop/testing/test/folder2/file006004.png"
        self.assertTrue(os.path.isfile(file))

    def test_folder2_count(self):
        x = len([name for name in os.listdir('/Users/lallepot/Desktop/testing/test/folder2')])
        self.assertTrue(x == 6)

    def test_folder3_1(self):
        file = "/Users/lallepot/Desktop/testing/test/folder2/folder2sub/20110724-130312.jpg"
        self.assertTrue(os.path.isfile(file))

    def test_folder3_2(self):
        file = "/Users/lallepot/Desktop/testing/test/folder2/folder2sub/20110916-153401_1.tiff"
        self.assertTrue(os.path.isfile(file))

    def test_folder3_3(self):
        file = "/Users/lallepot/Desktop/testing/test/folder2/folder2sub/20110916-153401.jpg"
        self.assertTrue(os.path.isfile(file))

    def test_folder3_4(self):
        file = "/Users/lallepot/Desktop/testing/test/folder2/folder2sub/20110916-153401.tiff"
        self.assertTrue(os.path.isfile(file))

    def test_folder3_5(self):
        file = "/Users/lallepot/Desktop/testing/test/folder2/folder2sub/file_3648_106886.png"
        self.assertFalse(os.path.isfile(file))

    def test_folder3_6(self):
        file = "/Users/lallepot/Desktop/testing/test/folder2/folder2sub/20110916-153401.png"
        self.assertTrue(os.path.isfile(file))

    def test_folder3_count(self):
        x = len([name for name in os.listdir('/Users/lallepot/Desktop/testing/test/folder2/folder2sub/')])
        self.assertTrue(x == 5)





import test_setup
import findnclean

if __name__ == '__main__':

    print("*** START ***")
    test_setup.setup()
    findnclean.main(0)
    unittest.main()

