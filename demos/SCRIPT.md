# Introduction
Today we're presenting and demonstrating our SEGP, a Platform as a Service for Imperial College
We have been developing this during this term under the guidance of Rob Chatley.

This project aims to develop a college-wide platform where students and staff can easily deploy their own (primarily web-based) software applications within the college or to the public.

We're going to demonstrate a couple of different use cases to see what you think - feel free to interrupt us with questions whenever.

# Setup
To get started using Impaas, I'll need to grab the CLI tool. Users can download binaries for Windows, macOS or Linux. I already have it installed using homebrew.

Now, I need to configure my CLI to point to our server (presumably, this would be on some imperial.ac.uk domain).

```sh
impaas remote add https://impaas.uk --set
```

Then, I'll log in to Impaas

```sh
impaas login
```

Which opens my browser and only lets me sign in using my college account.

Now I can see my details.

```sh
impaas user info
```

Users can be members of multiple teams and have different permissions in each.

# Demonstrations
## Static Site
Let's warm up by sharing a simple static blog with the public.
One could equally use GitHub Pages for this, which is free (for now).

`pushd blog`

Here I've got an HTML file and an image.

I'll create an app on Impaas, called blog, which uses the static 'platform' (more on that later).

```sh
impaas app create blog static -t demo
```

Then, I'll deploy all the files in my current working directory to the blog app

```sh
impaas app deploy -a blog .
```

Lo, and behold, going to [blog.impaas.uk](https://blog.impaas.uk) has my blog facing the public!

`popd`

## Dynamic Web App
Hosting dynamic web apps for free is where the Impaas value proposition shines. There are endless alternative ways to host, but most others require more hassle (such as setting up a cloud VM as a web server) or money (like Heroku, which got rid of their free tier).

`pushd greet`

Let's say now I have a "Hello world" app written in Python using Flask, and I want to deploy this to Impaas.
I have to add a Procfile, the same one that Heroku uses, to tell Impaas how to run my app.

Same as before:

```sh
impaas app create greet python -t demo
impaas app deploy -a greet .
```

Now let's visit [greet.impaas.uk](https://greet.impaas.uk) - works!

`popd`

## CI Deployments
`pushd greet-ci`

Let's say I now have this app on GitHub and I'm following good software practices by using a CI pipeline to run my tests. But I don't want to have to manually deploy to Impaas each time I make a change.

We've created a GitHub action to automatically deploy an application to Impaas.

I would add a stage to my CI workflow that looks like this, then I need to fill in the app name on Impaas (let's reuse greet from before). I also need to create a token to allow the CI pipeline to authenticate with Impaas so it can deploy to greet on my behalf.

```sh
impaas token create --id demo-ci-token -t demo
```

I'll add this as a secret in my repository

Now let's give this token permission to deploy my apps - we've already created a role called 'deployer' which gives only permissions for one app.

```sh
impaas role assign deployer demo-ci-token greet
impaas token show demo-ci-token
```

Let's make a dummy commit to our app and watch it deploy for us!

`popd`

## Container Deployments
### Using a Dockerfile
`pushd counter`

So far, we've seen two 'platforms' - static and python.
These are predefined using Dockerfiles and Buildpacks and will work for many common use cases.
Let's see what other platforms we have available

```sh
impaas platform list
```

Looks like there's NodeJS as well.

What if we're writing an app in a language that doesn't have a platform?
The general case is to containerise the app and deploy the image.

Say I have a small web app written in Go, which doesn't have a respective platform available.

```sh
impaas app create counter static -t demo
```

We write a Dockerfile to package our app into a container image - Impaas will pick that up and use it to build and deploy our application!

```sh
impaas app deploy -a counter --dockerfile .
```

And we can see [counter.impaas.uk](https://counter.impaas.uk) is up and running!

## From a Registry
We can deploy any image from the Internet - this one happens to be an admin dashboard which from the official Docker Hub

```sh
impaas app create dashboard -t demo
impaas app deploy -a dashboard --image tsuru/dashboard
```

Now [dashboard.impaas.uk](https://dashboard.impaas.uk) seems to be working!

This extends to CI as well - if a user has an existing project which is already containerised and has a pipeline that pushes to a registry (such as the official Docker Hub or GitHub Container Registry), all they need to do is add our deploy stage and give it the image tag.

`popd`

## Databases
`pushd todo`

Many web applications will be backed by, or eventually want to be backed by a database.

We have implemented the capability to add what are called 'services' to apps on the platform.

So let's walk through how it would work for a user.

Let's say here I've developed a simple to-do list app that uses a MySQL database to store my information.
I've been developing and testing it locally, perhaps by installing MySQL server onto my machine.

Now, I'm ready to show my brilliant to-do list to the world.
So, what do I do? Stay with me here...

First, I'll create a new app on Impaas for my project

```sh
impaas app create todo python -t demo
```

At this point, I could deploy my Flask app as before, but my app wouldn't have a database to use!

Let's see if MySQL is available on the platform...

```sh
impaas service plan list mysql
```

Great! Looks like Impaas can provision me a MySQL instance - let's make one called tododb in the demo team

```sh
impaas service instance add mysql tododb -t demo
impaas service instance info mysql tododb
```

OK, so now I have a fresh MySQL database... somewhere. But how can I use it?

I need to 'bind' the tododb MySQL instance to my todo app

```sh
impaas service instance bind mysql tododb -a todo
```

These environment variables are now available within my todo app. I'll now adjust my app code to build the DB connection string using os.getenv instead of localhost

Now, I'm ready to deploy!

```sh
impaas app deploy -a todo .
```

Let's give it a minute... Great! Now, all of you can visit [todo.impaas.uk](https://todo.impaas.uk) on your own devices and mess around with my very important list of tasks.

We aren't limited to providing just MySQL databases!
Impaas could also offer Redis, Elasticsearch, or whatever you want really - although we expect the most useful ones will be the various database servers (MySQL as shown, Postgres, MongoDB etc.)

Since all a service does is provision an instance of something, somewhere, and set environment variables when bound to an app, we just need to write new logic to provision new instances and give back the relevant values.
In fact, the database in this example aren't even running on the same cluster as the app - they're running on a separate machine in Azure.

As such, these services are fully extensible and can be hosted wherever is most appropriate.

`popd`

# File Storage

`pushd filemgr`

Similarly, some apps may wish to make use of file storage.
This is available in Impaas via 'volumes'.

Let's say I've built a simple file manager app, again using Python and Flask, and I want to deploy it to Impaas.

```sh
impaas app create filemgr python -t demo
impaas app deploy -a filemgr .
```

Now this is up and running, but it gives us an error since it can't find the directory it stores its files in (which is /uploads)

We create a volume with

```sh
impaas volume create uploads azurefile -t demo -o capacity=512Mi -o access-modes=ReadWriteMany -p local
```

Then, we 'bind' it to our app which mounts it within the app at the given directory

```sh
impaas volume bind uploads /uploads -a filemgr
```

Volumes automatically create new file storage objects in Azure, which keeps everything self-contained.

`popd`

# Permissions and Quotas

As mentioned earlier, the RBAC in Impaas is granular, allowing us to set or unset specific permissions per team, per user, or overall defaults.

We could allow teams to run apps with services but not provision storage volumes, or only allow one user in a team to see and restart apps but not modify or remove them, and have administrators who can see and set roles for permissions platform-wide, and course leaders who can create or delete teams, manage the users within them etc.

App resource quotas can also be set, for instance, to limit a team to only 5 running apps at once.

For services, we can configure multiple plans for one type of service, for instance, a MySQL DB instance plan with 1 gig of storage, another with 5 gigs of storage, etc.

And for volumes, we can set overall or team-level resource limits on how much storage can be provisioned.

# Administration

We have designed a proof-of-concept administration interface called 'Impaas Manager', aimed to be used by course leads within departments to automatically bulk create and manage groups with students in them.

Here's what it looks like (we'd eventually like this to be hosted on Impaas itself so it's completely self-contained, but unfortunately our development cluster isn't powerful enough).

A course leader would see all their active courses here.
To create a new one, they would upload this standard YAML format which lists all the groups by number and the members by shortcode, and optionally if they want the groups in this course to have access to database services and/or storage volumes.

After uploading, it's ingested by Impaas and bulk creates all these teams!

Under a course, the leader can see the permissions (which are easily togglable), groups and their members (which are easily added or removed, such as when a student drops a module).

After the course has ended, the leader would flush out all of the groups to get rid of any lingering apps and teams.

# Architecture

Everything you've seen today is hosted on Azure.

The platform itself runs in a managed Kubernetes cluster using AKS, which vastly reduces the operational and administrative load in a production use case.

User deployments run in pods (containers) across pools of Azure VMs, which are configurable in size depending on budgets and automatically scale with system load - saving us money when the system isn't used for heavy workloads. The pods are rootless which provides isolation and security guarantees.

Authentication is handled via Microsoft Entra (formerly Azure AD), using OAuth2, which allows us to leverage the college's existing user management and SSO.

We've also got TLS termination configured across the board, so all traffic is encrypted in transit. LetsEncrypt Certificates are automatically provisioned and on the fly and renewed when neede, but we could also use Imperial's own CA if we wanted to.

Tsuru is an existing open-source project written in Go - we have forked it to allow it to work on Azure and extended it to add extra functionality more specific to Imperial's use case.

# Any Questions?
