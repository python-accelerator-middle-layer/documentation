Documentation for Python Accelerator Middle Layer.

The documentation follows the [Diataxis approach](https://diataxis.fr/).

## Building the Docs

1. Create a virtual environment and activate it.
2. Install the requirements with `pip install -r requirements.txt`.
3. Build the docs locally with `./build-docs.sh`. The new version is available in `docs/build/html/index.html`.
4. When the local version looks good, push your changes. Pushes to main will build and deploy the new version.

```{note}
For the notebooks it is necessary to have the required pyAML packages installed in the environment.
If you add a new dependency remember to also add it in the requirements.txt.
```

## Where to Place Content

Content should be placed in these categories:

#### [Tutorials](https://diataxis.fr/tutorials/)

A tutorial is a practical activity where learning is done by doing something meaningful towards an achievable goal.
The purpose is not to get something done but to help to learn.

It should be structured as a lesson. The recommended format is to use a Jupyter notebook.

#### [How-to guides](https://diataxis.fr/how-to-guides/)

How-to guides help to get something done in the correct and safe way.
The focus should be on how to achieve a specific task.

Details of the difference between tutorials or how-to guides can be found at https://diataxis.fr/tutorials-how-to/#tutorials-how-to 
if you are unsure where to place your content.

#### [Technical reference](https://diataxis.fr/reference/)

Technical references are technical descriptions of the software, for example the API.

It is content where the user can look up information but is not meant to read everything.

#### [Explanation](https://diataxis.fr/explanation/)

Explanations have the purpose to deepen and broaden the understanding of a topic.

They provide background and context for why thing are done in a specific way,
for example design decisions, technical constraints etc.

It can also contain details about alternatives and the reason why one specific alternative was chosen.
