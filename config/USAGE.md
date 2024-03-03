# Imperial PaaS - Getting Started

This guide will show you how to deploy a simple web app to **Imperial's Platform as a Service** (PaaS).<br>
This will allow you to host your web app online, accessible to anyone with an internet connection.

## Making an App

Let's start by making a simple web app.

Make a folder on your desktop to store your web app, such as `my-website`.

Find any picture (online, or one you've taken yourself) and save it in the folder.

Open a text editor and paste the following code into the file (don't worry about understanding it for now):
```html
<!DOCTYPE html>
<html>
  <head>
    <title>My App</title>
  </head>
  <body>
    <h1>Hello, world!</h1>
    <p>This is my first web app.</p>
    <p>Here's an image:</p>
    <img src="image.jpg">
  </body>
</html>
```
Change `image.jpg` to the name of the picture you saved in the folder.

Save this document as `index.html` in the same folder as the picture.<br>
*Note: in TextEdit on macOS, select `Format` > `Make Plain Text` before saving.*

Your folder should now look like this:
```
my-website/
  image.jpg
  index.html
```

## Installing `impaas`

Next, you need install a command-line (text-based) tool that will let you deploy your web app to Imperial's PaaS.<br>
Let's install it on your computer.

To start, open the Terminal app on your computer.<br>
You can find it by searching for "Terminal" or "Command Prompt" in the search bar.

Then, paste the following commands into the terminal and press `Enter`:
```bash
curl -fsSL "https://tsuru.io/get" | bash
echo "alias impaas='tsuru'" >> ~/.bashrc
source ~/.bashrc
```

If all went well, you should now have the `impaas` command available in your terminal!

## Configuring `impaas`

Now we need to tell `impaas` about Imperial's PaaS. Run the following command:
```bash
impaas target add impaas https://impaas.uk -s
```

Now you need to log in to your Imperial account, with:
```bash
impaas login
```
This should open a web page in your browser. Log in with your Imperial username and password.<br>
When you see "Login Successful", you can close the browser tab and return to the terminal.

## Deploying Your App

Now you're all set to deploy your app to Imperial's PaaS.

In the terminal, navigate to the folder where your app is stored. For example, if you made a folder called `my-website` on your desktop, you can get there with the following command:
```bash
cd ~/Desktop/my-website
```

Next, let's create a new app on the PaaS, in this case called `my-app` (ignore the `static` part):
```bash
impaas app create my-app static
```
*Note that if someone else has already created an app with the same name, you will need to choose a different name.<br>
You can put your Imperial username in the app name to make it unique, for example `my-app-abc123`.*

Finally, deploy your app to the PaaS (don't forget the `.` at the end!):
```bash
impaas app deploy -a my-app .
```
This might take a few minutes to complete.

Once it's done, you can check the status of your app with the following command:
```bash
impaas app info -a my-app
```

This will give you a lot of information about your app.<br>
The part we're interested in is the "External Addresses" section:
```
Application: my-app
...
External Addresses: my-app.impaas.uk:443
Created by: abc123@ic.ac.uk
...
```

Open your web browser and go to the URL listed under "External Addresses" (in this case, [https://my-app.impaas.uk](https://my-app.impaas.uk)).

You should now see your web app live on the internet!<br>
You can share this link with anyone and they will be able to see it too.
