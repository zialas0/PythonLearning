class Calendar:
    def __init__(self):
        self.appts = []

    def is_free(self, date, start, end):
        free = True
        for d, s, e, _ in self.appts:
            if d == date and (end > s
                              or start < e):
                free = False
        return free

    def is_busy(self, date, start, end):
        return not self.is_free(date, start, end)

    def schedule_time(self, date, start, end, name):
        if self.is_free(date, start, end):
            self.appts.append((date, start, end, name))
            self.appts.sort(key=lambda x: (x[0], x[1]))
            return True
        return False

    def delete_event(self, name):
        count = len(self.appts)
        self.appts = [a for a in self.appts if a[3] != name]
        if len(self.appts) == count:
            return f"Event '{name}' not found."
        else:
            return f"Event '{name}' deleted successfully."
    

c = Calendar()

print(c.schedule_time(12, 1, 3, "person1"))
print(c.schedule_time(12, 2, 4, "person2"))
print(c.schedule_time(12, 4, 5, "person1"))
print(c.schedule_time(12, 1, 2, "person3"))
print(c.schedule_time(12, 9, 11, "person2"))

print(c.is_busy(12, 3, 4))
print(c.is_busy(12, 3, 5))
print(c.appts)
print(c.delete_event("person2"))