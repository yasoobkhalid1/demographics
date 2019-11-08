#
# Class that preprocesses image for training/classification by
# detecting the largest face in an image, cropping it, and aligning it
#

import os
import dlib
import glob
import cv2

class Preprocessor():

    def __init__(self, output_folder, file_path):

        self.output_folder = output_folder

        self.file_path = file_path
        models_path = self.file_path + "/models/"

        # The facial landmarks training file to identify the landmarks on the detected img
        # sourced from: http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2
        landmark_training_name = 'shape_predictor_68_face_landmarks.dat'
        predic_path = os.path.join(models_path, landmark_training_name)

        # Load all the models we need: a detector to find the faces, and a shape predictor
        # to find face landmarks so we can precisely localize the face
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(predic_path)

    def preprocess(self, inp_path):
        """
        Detects the face present inside an image and preprocesses it by cropping,
        aligning, and stretching the face according to the specified dimensions.
        :param inp_path: The path to the original image
        :type inp_path: string
        :return: A numpy array containing the aligned RGB image
        :rtype: numpy.ndarray[(rows,cols,3),uint8]
        """

        # reads the image file and converts it into an RGB array
        image = cv2.imread(inp_path, 1)

        # if image file is corrupted, put file into corrupted folder
        if image is None:
            os.rename(inp_path, self.output_folder + '\\corrupted')
            return 'corrupted'

        # Ask the detector to find the bounding boxes of each face. The 1 in the
        # second argument indicates that we should upsample the image 1 time. This
        # will make everything bigger and allow us to detect more faces.
        faces = self.detector(image, 1)

        # if no faces detected, put file into faceless folder
        if len(faces) == 0:
            os.rename(inp_path, self.output_folder + '\\faceless')
            return 'faceless'

        # select the largest face out of all the faces in the image
        face = max(faces, key=lambda rect: rect.width() * rect.height())

        # Get the landmarks/parts for the face in box face.
        face_landmarks = self.predictor(image, face)
        aligned_img = dlib.get_face_chip(image, face_landmarks)
        return aligned_img

    def batch_preprocess(self, inp_folder):
        """
        Batch preprocesses all the images in the inp_folder, detecting
        the face present inside each image and preprocessing it by cropping,
        aligning, and stretching the face according to the specified dimensions.
        :param inp_folder: The path to the folder containing all images
        :type inp_folder: string
        """

        # the directory name containing all the image data
        # default folder path is used to test only the sample
        input_folder_path = os.path.join(self.file_path, inp_folder)

        # list of all the images contained within the input_folder_path
        img_paths = glob.glob(os.path.join(input_folder_path, '**/*.jpg'), recursive=True)

        # array of all preprocessed images
        imgs_array = []

        for inp_img_path in img_paths:

            pre_processed_img = self.preprocess(inp_img_path)
            imgs_array.append(pre_processed_img)

        return imgs_array



