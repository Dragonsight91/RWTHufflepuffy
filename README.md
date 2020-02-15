# Usage

## Syntax

```none
{command} {action} {params}
```

## Available Commands

- [feature](#feature)
- [vote](#vote)
----
## Commands

- ## `$feature`

  ### Actions

  - `$feature add {text}`

    Adds `text` as feature request to the Database.

  - `$feature purge`

    purges the feature Request DB

- ## `$vote`
  Create or remove votes. Votes are done by reacting.

  ### Actions
    - `$vote create {name};{options}`
      
      Adds a vote named {name} with voting options {options}.
      Options must be comma separated.

      Examples:
      - create a yes/no vote with title **Should I?**
        **Command**
        ```none
        $vote create Should I?;yes,no
        ```
        **Output**
        ```none
        
        ```

      - create a 
    -   