# FootGPT

FootGPT is a project that aims to build a football news language model using the Generative Pretrained Transformer (GPT) architecture. The project is based on Andrej Karpathy's [YouTube video](https://www.youtube.com/watch?v=kCc8FmEb1nY) and makes use of some codes from his [NanoGPT repository](https://github.com/karpathy/nanoGPT).


The data used to train `FootGPT` is a small 14K dataset of football news articles sourced from the internet. This data is used for educational purposes to demonstrate the application of machine learning in the realm of football journalism. By using this data, the model is able to learn the writing style and terminology used by professional football journalists. This makes it possible to generate realistic and coherent text that closely resembles the output of human writers. 


## How to use FootGPT

FootGPT have been trained on a Google Colab GPU and the model weigh is just 50 MB.

To use FootGPT, you can either use built-in FastAPI web app or use the model directly in your own code. 

### Using the FastAPI web app

The FastAPI web app can be run locally or on a server. To run the web app locally, you can use the following command:

    uvicorn main:app --reload

Currently, there is no hosted version of the web app.

API documentation can be found at http://localhost:5000/docs 

`playground` folder contains a simple react app that can be used to interact with the API. To run the app, you can use the following command:

    npm install
    npm run dev

The app can be accessed at http://localhost:5173

### Screenshots

![screenshot1](https://i.imgur.com/5aGiXqS.png)

![screenshot2](https://i.imgur.com/GKtszNx.png)

![screenshot3](https://i.imgur.com/xwIVm1y.png)


## Notes

Since the model is trained on a small dataset, the results are not perfect. However, the model is able to generate coherent text that closely resembles the output of human writers.