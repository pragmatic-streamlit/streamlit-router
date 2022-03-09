# streamlit-router

## Install

```
pip install streamlit-router
```

## Example

```
    def index(router):
        st.text("fron page index")
        x = st.number_input("task id")
        if st.button("create task"):
            router.redirect(*router.build("create_task", {"x": x}))
        if st.button("cancel task"):
            router.redirect(*router.build("cancel_task", {"x": x}))
        if st.button("view task"):
            router.redirect(*router.build("view_task", {"x": x}))
        st.text("others on page index")

    # variable router auto inject if as first params
    def cancel_task(router, x):
        st.text(f"fron page cancel task x={x}")
        if st.button("back to index"):
            router.redirect(*router.build("index"))
        st.text("others on page cancel task")

   # variable router auto inject if as first params
    def create_task(x, router):
        st.text(f"fron page create task x={x}")
        if st.button("back to index"):
            router.redirect(*router.build("index"))
        st.text("others on page create task")

    router = StreamlitRouter()
    router.register(index, '/')
    router.register(cancel_task, "/tasks/<int:x>", methods=['DELETE'])
    router.register(create_task, "/tasks/<int:x>", methods=['POST'])

    # deco also works
    @router.map("/tasks/<int:x>")
    def view_task(x):
        st.text(f"fron page view task x={x}")
        if st.button("back to index 2"):
            router.redirect(*router.build("index"))
        st.text("others on page view task")

    router.serve()
```