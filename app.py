from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from peewee import *

app = Flask(__name__)
matplotlib.use("Agg")

db = SqliteDatabase("students.db")

class Students(Model):
    name = CharField()
    age = IntegerField()
    subject = CharField()
    grade = IntegerField()
    hours_per_week = IntegerField()

    class Meta:
        database = db

db.connect()
db.create_tables([Students])

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/plots", methods=["GET", "POST"])
def plots():
    students = Students.select()
    if not students:
        return redirect(url_for("upload"))
    
    df = pd.DataFrame([s.__data__ for s in students])

    # atzīmju sadalījums
    plt.figure()
    plt.hist(df["grade"], bins=10, edgecolor="black", alpha=0.7)
    plt.title("Atzīmju sadalījums")
    plt.xlabel("Atzīme")
    plt.ylabel("Biežums")
    plt.savefig("static/plots/histogram.png")
    plt.close()
    
    # mācību stundas vs. atzīme
    plt.figure()
    plt.scatter(df["hours_per_week"], df["grade"], c="blue", alpha=0.5)
    plt.title("Macību stundas pret atzīmes")
    plt.xlabel("Stundas nedēļā")
    plt.ylabel("Atzīme")
    plt.savefig("static/plots/scatter.png")
    plt.close()
    
    # atzīmju sadalījums pēc priekšmeta
    plt.figure()
    df.boxplot(column="grade", by="subject", grid=False)
    plt.title("Atzīmju sadalījums pēc priekšmeta")
    plt.xlabel("Priekšmets")
    plt.ylabel("Atzīme")
    plt.xticks(rotation=45)
    plt.savefig("static/plots/boxplot.png")
    plt.close()
    
    # vidējais vērtējums par priekšmetu
    plt.figure()
    df.groupby("subject")["grade"].mean().plot(kind="bar", color="green", edgecolor="black")
    plt.title("Vidējais vērtējums par priekšmetu")
    plt.xlabel("Priekšmets")
    plt.ylabel("Vidējais vērtējums")
    plt.savefig("static/plots/bar_chart.png")
    plt.close()
    
    # 5 labākie skolēni pēc vertējumiem
    top_students = Students.select().order_by(Students.grade.desc()).limit(5)
    
    return render_template("plots.html", top_students=top_students)

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        file = request.files["file"]
        if file and file.filename.endswith(".csv"):
            df = pd.read_csv(file)
            Students.delete().execute()
            for _, row in df.iterrows():
                Students.create(
                    name = row["name"],
                    age = row["age"],
                    subject = row["subject"],
                    grade = row["grade"],
                    hours_per_week = row["hours_per_week"]
                )
            return redirect(url_for("plots"))
    return render_template("upload.html")

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)