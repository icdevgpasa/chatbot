# Core
Time of building models locally around `5 min`.
Time of response `40 ms` +/- `5 ms`, response size `241 B`.


# How to start

## Init Env
``` bash
$ pip3 install rasa
```

## To train the model

``` bash
    $ make train-model
```

## To run server locally [[src1]](https://rasa.com/docs/rasa/command-line-interface#rasa-run)
print command bellow

``` bash
    $ make run-rasa-server

    # or 

    $ rasa run \
        --enable-api \
        -vv \
        --log-file out.log
```


## To run server on docker
print command bellow

``` bash
    $ ./run.sh
```

## To ask the server [[src1]](https://rasa.com/docs/rasa/http-api) [[src2]](https://rasa.com/docs/rasa/pages/http-api)

``` bash
    $ curl 0.0.0.0:5005/webhooks/rest/webhook  -d '{"sender": "SESSION_ID", "message": "hi can you help me ?"}' | json_pp
```

### To get Intent, intent_ranking and Entity probability
``` bash
    $ curl 0.0.0.0:5005/model/parse -d '{"text": hi can you help me ?", "message_id": "b2831e73-1407-4ba0-a861-0f30a42a2a5a"}' | json_pp
```

# Quick info About Rasa
## Information
1. `data/nlu.md` store all the training data, all the intents.
2. `data/stories.md` store all the dialogs examples (skills)
3. `domain.yml` list off all intents, entities, responses and actions.
4. `config.yml` NLU pipeline configurations and model details.
5. `actions.py`
6. `credentials,yml` token for external systems.
7. `endpoints.yml` allow rasa to communicate with other systems.
7. `test/*` all files for testing.

## rasa commands

``` bash
$ rasa train
```

``` bash
$ rasa interactive
```

## actions

### Form action
* `required_slots()` mandatory, all slots that make up the form.
* `slot_mappings()` optional, how to fill each slot.
* `submit()` mandatory, what to do when the form is complete.

to build form we will use 
1. domain.yml
    1. create slots.
    2. Register new intents and entities.
    3. Add response templates.
    4. Register form name.
2. nlu.md
    1. Training data for intent and entities.
3. stories.md
    1. Add stories to shoe the assistant how to activate and deactivate the form.
4. actions.py
    1. Write code to control the form's behavior.
5. config.yml
    Add the FormPolicy to the policy configuration.
6. endpoints.yml
    1. Expose the action server endpoint.

## Command Line Interface

```
rasa run \
    --enable-api \
    -vv \
    --log-file out.log
```

## Good tips
1. after creating new intent register them on `domain.yaml` one `intents` section


## URLS
https://legacy-docs.rasa.com/docs/platform/api/models/#

https://rasa.com/docs/rasa-x/installation-and-setup/install/local-mode
https://www.youtube.com/watch?v=us8QJD_5SUU&ab_channel=InnovateYourself


https://rasa.com/docs/rasa/how-to-deploy/

https://www.youtube.com/watch?v=dL7zbY4eULA&ab_channel=InnovateYourself




# WhatsApp
https://www.youtube.com/watch?v=gLt8j8ebDK8&ab_channel=InnovateYourself