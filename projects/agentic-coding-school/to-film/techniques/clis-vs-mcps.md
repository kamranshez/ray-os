Use this talk too: [https://www.youtube.com/watch?v=v3Fr2JR47KA](https://www.youtube.com/watch?v=v3Fr2JR47KA) from 6 mins in (mention that they may make improvements here)

Easier to chain in a CLI because you can have the output go to another thing easily without going into the context window or write it directly to a file

CLI pairs well with the monitor tool allowing for streaming data / trailing logs.

As always depends on the design :) but making a cli is extremely easy and you can sdout very custom things for LLMs which are token efficient compared to what humans need.

Good for poorly designed MCPs too but have to make it aware of it. Can do more things like stdout to a file so it’s not loaded into the context window unlike MCPs 

Bento CLI as an example

Can also stream with a CLI so you can do things like set up monitors

---

Eric Zakariasson take ([source](https://x.com/ericzakariasson/status/2066570396183548350)) — uses both daily, they serve different purposes:

> mcp > cli
>
> im glad this debase is not as active anymore. i use both every day. they just serve different purposes
>
> cli for stuff the model already knows. git, gh, npm, docker, file ops. trained on man pages, and costs almost nothing in context. if im already signed in locally theres no reason to wrap it in anything
>
> mcp for most integrations. slack, notion, linear, twitter
>
> and its neat to have a protocol for all these integrations
> - add one server to my teams cursor and everyone gets access
> - auth once, persists, same locally and in cloud
>
> it also just feels better in cursor. rich icons, traceable, you can easily follow whats happening (tbh not reading that much)
>
> cli for personal, mcp for team (with oauth)
