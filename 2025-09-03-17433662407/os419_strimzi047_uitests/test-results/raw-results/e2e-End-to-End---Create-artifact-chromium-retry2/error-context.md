# Page snapshot

```yaml
- generic [ref=e2]:
  - heading "Application is not available" [level=1] [ref=e3]
  - paragraph [ref=e4]: The application is currently not serving requests at this endpoint. It may not have been started or is still starting.
  - generic [ref=e5]:
    - paragraph [ref=e6]: "i Possible reasons you are seeing this page:"
    - list [ref=e7]:
      - listitem [ref=e8]:
        - strong [ref=e9]: The host doesn't exist.
        - text: Make sure the hostname was typed correctly and that a route matching this hostname exists.
      - listitem [ref=e10]:
        - strong [ref=e11]: The host exists, but doesn't have a matching path.
        - text: Check if the URL path was typed correctly and that the route was created using the desired path.
      - listitem [ref=e12]:
        - strong [ref=e13]: Route and path matches, but all pods are down.
        - text: Make sure that the resources exposed by this route (pods, services, deployment configs, etc) have at least one pod running.
```