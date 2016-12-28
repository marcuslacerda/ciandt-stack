# Stack Gallery

Stack is a tool that shows technology used in your product. There is a strong integration with [Tech Gallery][techgallery] and [Knowledge Map][knowledge]

![screenshot from 2016-10-27 13-02-19](https://cloud.githubusercontent.com/assets/6742877/19829377/e83e0b94-9dbd-11e6-84d8-cbad124c8e0f.png)

## Local installation (recommended for normal developers)
You need [Git][] tool for clone this repository:

```console
$ git clone https://github.com/marcuslacerda/stack-gallery.git
```

Then, you must use [Python 2.7.9 ][Python] to install the following all libraries required:

```console
$ cd stack-gallery/app
$ pip install -r requirements.txt
```
If you don't have python local environments, you could use docker environment describe below.

You must define these environments on your variable.
```console
$ export GOOGLE_CLIENT_ID=set-google-client-id-here_or_export-env-vavariable>
$ export GOOGLE_CLIENT_SECRET=set-google-client-secret-here_or_export-env-vavariable>
$ export ELASTICSEARCH_URL=url-to-elasticsearch-stack
```

At last, you can start the local web server using this command

```console
$ cd app
$ python run.py
```

## Running (by docker)
You must install [Docker][] on your environment. After you can build the image using the following command.

```console
$ git clone https://github.com/marcuslacerda/stack-gallery.git
$ docker build -t stack-app:latest .
```

Run the Docker container using the command shown below.

```console
$ docker run -e ELASTICSEARCH_URL=http://localhost:9200 -e GOOGLE_CLIENT_SECRET=<put-your-client-secret> -e GOOGLE_CLIENT_ID=<put-your-client-id> -p 5000:5000 stack-app
```

If you need a full local enviroment, you must start [Elasticsearch] and change elasticsearch host at ELASTICSEARCH_URL variable.

You must configure these GOOGLE values from [Google APIs console]

```console
$ run docker -p 9200:9200 elasticsearch
```

To execute tests, install all dependencies from requirements_test.txt into lib_tests path:
```
pip install -r requirements_test.txt -t lib_tests
```

To run the tests
```console
$ nosetests -v tests
```
#### Coverage:

To measure tests coverage in Python code. This recipe runs nosetests suite and presents coverage at the end:
```
nosetests -v --with-cover --cover-html --cover-package=. tests/
```
A detailed report from coverage can be found at cover folder in project's path.


The application will be accessible at http://localhost:5000

[Docker]: https://docs.docker.com/engine/installation
[Google APIs console]: https://code.google.com/apis/console
[techgallery]: https://github.com/ciandt-dev/tech-gallery
[knowledge]: https://github.com/marcuslacerda/tech-gallery-knowledgemap
[Git]: http://help.github.com/set-up-git-redirect
[Python]: https://www.python.org
[Pull requests]: https://help.github.com/categories/collaborating-on-projects-using-issues-and-pull-requests/
[Elasticsearch]: https://www.elastic.co/products/elasticsearch
