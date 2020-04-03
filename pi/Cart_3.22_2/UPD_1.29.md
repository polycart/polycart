# Update_1.29

The **"Widget Deviation"** puzzled me several days, it has many puzzling things such as if we turn the **fullscreen** off and change the size of the window, the abnormal **widget** will move to where it should be.

I found the following things might cause **"Widget Deviation"**:

1. put the **Widget** directly into a **Screen** and set its *center* with a link to its parent

2. set the *size* (including *height*) of the **Widget** with a link to its parent and set its *center* with a link to its parent

So, as I saw other projects usually make the page as a **Widget** and put it into a **Screen**  ~~(I don't know why but it really avoided the "Widget Deviation")~~

All in all, the update includes:

* change the base class of **DefaultScreen** from **Screen** to **Widget**

* create a new class **DefaultGridLayout** to default the size or other properties of  **GridLayout**
* in **CartApp**.build(), declare a **Screen** and put the **MainScreen(Widget)** in, then put it in the **sm(ScreenManager)** 
* other small changes such as *font_size* and *show_cursor*, blabla...