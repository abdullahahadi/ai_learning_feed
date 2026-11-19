# Architecture

This page describes where the project is heading and the rules that keep its parts separate. It covers the target design, what exists today, and the order of the work.

## Two planes

The system is split into two planes that live in different repositories.

| | Engine plane (this repo) | Client plane (separate repo, later) |
|---|---|---|
| Job | Produce a good feed for a given learner profile | Serve people |
| Contains | Collector, researcher, item store, curator, prompts | Sign-up, login, profiles, bot, delivery |
| Knows about | Items, sources, scores | Users, accounts, channels |
| Faces | Other services only, on a private network | The public |
| Changes when | Sources, ranking or the model change | The product or its users change |

This repo is the engine plane. It has no users, no user management and no authentication.

## The contract between the planes

```text
client plane  --  profile + opaque id  -->  engine plane
client plane  <--------  feed  -----------  engine plane
```

- The client sends a learner profile and an id.
- The engine returns a feed.
- The id lets the engine remember what a learner already received. The engine cannot tell who is behind it.
- Neither side depends on how the other works inside. Either can be rebuilt as long as these shapes stay the same.

Because the engine has no authentication, it must only be reachable on the private network between services. No port is published to the internet.

## Inside the engine

```text
 collector ----> item store <---- researcher
 free sources,   items,           AI search per profile:
 own schedule    sent history     plan, search, read, decide, stop
                     |
                  curator      filter (code) -> score (model) -> rank (code) -> check (code)
                     |
                    feed
```

| Part | Job | Uses the model |
|---|---|---|
| Collector | Fetches items from plug-in sources on its own schedule | No |
| Researcher | Searches for what a profile is missing, in a controlled loop with limits | Yes |
| Item store | The database the services share: items and what was already sent | No |
| Curator | Chooses and orders the items for one profile | Yes, for scoring only |
| Model client | The single module that talks to the model provider | n/a |

## Rules

1. **Each service does one job** and knows nothing about how the others work inside.
2. **Services share only a small contract:** the typed data they pass to each other. It is defined in one shared place.
3. **A service never depends on another service,** only on the shared contract.
4. **Everything that finds items writes the same typed item.** The curator does not know which source an item came from.
5. **The model never writes a link.** It scores items by id, or picks from pages a tool actually opened.
6. **Code does the cheap work first.** The model only receives what needs judgment.
7. **Parts are pluggable:** sources in the collector, steps in the curator, tools in the researcher.
8. **Prompts are templates kept as files,** assembled at run time from the instruction, the profile, the current context and the task. Each run records the template version it used.
9. **Nothing is hardcoded.** Configuration comes from settings.
10. **Every run leaves a record** of what came in, what was dropped and why, and what the model was asked.
11. **One part failing does not stop the feed.**

## Today

The engine currently runs as a single pipeline that starts, finishes and exits:

```text
search (model with web search)  ->  curate (one model call)  ->  deliver (Telegram)
```

- Search and curation are each one model call with a fixed prompt.
- Search hands curation a block of free text.
- Configuration is spread over several modules.
- Delivery to Telegram lives here as a stand-in for the client plane. It depends only on the feed and may move out of this repo later.

## Roadmap

Each step is one change and one pull request, and each leaves the app working.

| Step | Change | Issue |
|---|---|---|
| 1 | One settings module | #9 |
| 2 | Curator as a pipeline of small steps | #10 |
| 3 | Prompts as versioned templates | not opened yet |
| 4 | uv workspace with one package per service | #11 |
| 5 | Database for items and sent history | not opened yet |
| 6 | Collector with plug-in sources | not opened yet |
| 7 | Researcher service | not opened yet |
| 8 | Internal interface that takes a profile and returns a feed | not opened yet |

## Not decided yet

- The form of the internal interface in step 8.
- When delivery moves to the client plane.
- The limits and schedule for the researcher.
