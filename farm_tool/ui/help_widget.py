# This Python file uses the following encoding: utf-8

from PySide6.QtWidgets import (QDockWidget, QTreeWidget, QTreeWidgetItem)


class HelpWidget(QDockWidget):
    def __init__(self, main_window):
        QDockWidget.__init__(self, "Help Window", main_window)

        helpTreeW = QTreeWidget()
        helpTreeW.setColumnCount(1)
        helpTreeW.setHeaderLabels(["Tabs"])

        data = {
            "Groups": ["Please enter the name of your groups.\n For example, you could have a horse barn you call \"main barn\" or a \n"
            +"group of chickens and geese you refer to as the \"birds\". The group that \n you create will have all of its expenses reported together, so group them accordingly."],
            "Animals": ["Please add an animal by entering its \n name. Select the group according to how you want to display its expenses. \n"+
            "The date added field should be the date that the animal was added to your \n farm, whether it was born or purchased.\n"+
            "Starting from the date added your animal's expenses will appear in the report."],
            "Schedules": ["This section is where you can add \nrepeating expenses for your animals. For example, you may list\n"+
            "amounts that you use to feed animals every morning or evening.\n"],
            "Supplies": ["Please enter supplies that you use for scheduled feedings."],
            "Expenses": ["This section is where you can add \nexpenses for your animals or groups. For example, you may have\n"+
            "an electric bill that covers the water heaters in a whole barn\n or a vet bill for one animal.\n"],
        }

        items = []
        for key, values in data.items():
            item = QTreeWidgetItem([key])
            for value in values:
                ext = value.split(".")[-1].upper()
                child = QTreeWidgetItem([value, ext])
                item.addChild(child)
            items.append(item)

        helpTreeW.insertTopLevelItems(0, items)

        #helpTreeW.append("item1")
        #helpTreeW.append("item2")
        #helpTreeW.append("item3")
        helpTreeW.show()

        self.setWidget(helpTreeW)
        self.setFloating(False)
