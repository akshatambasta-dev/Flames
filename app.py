from flask import Flask, render_template, request

app = Flask(__name__)


def rm_common(a, b):
    # Original helper function: remove one matching character from each name.
    for i in range(len(a)):
        for j in range(len(b)):
            if a[i] == b[j]:
                char = a[i]
                a.remove(char)
                b.remove(char)
                return (a + ["*"] + b, True)

    return (a + ["*"] + b, False)


def calculate_flames(player1_name, player2_name):
    """Run the supplied FLAMES algorithm using names from the web form."""
    # Match the original input preparation.
    n1 = list(player1_name.lower().replace(" ", ""))
    n2 = list(player2_name.lower().replace(" ", ""))

    if not n1 or not n2:
        return None

    # Remove common letters until there are no matches left.
    cont = True
    while cont:
        lst, cont = rm_common(n1, n2)
        idx = lst.index("*")
        n1 = lst[:idx]
        n2 = lst[idx + 1:]

    # Count letters remaining in both names.
    cnt = len(n1) + len(n2)

    # Original FLAMES relationship list.
    res = [
        "Friends",
        "Lovers",
        "Affectionate",
        "Marriage",
        "Enemies",
        "Siblings"
    ]

    # Original elimination logic, kept unchanged.
    while len(res) > 1:
        split_index = (cnt % len(res)) - 1

        if split_index >= 0:
            right = res[split_index + 1:]
            left = res[:split_index]
            res = right + left
        else:
            res.pop()

    return {
        "relationship": res[0],
        "remaining_letters": cnt,
    }


@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    error = None
    player1 = ""
    player2 = ""

    if request.method == "POST":
        player1 = request.form.get("player1", "").strip()
        player2 = request.form.get("player2", "").strip()

        # Reject empty or spaces-only names with a friendly message.
        if not player1.replace(" ", "") or not player2.replace(" ", ""):
            error = "Please enter both names using at least one letter."
        else:
            result = calculate_flames(player1, player2)
            if result is None:
                error = "Please enter valid names."

    return render_template(
        "index.html",
        result=result,
        error=error,
        player1=player1,
        player2=player2,
    )


if __name__ == "__main__":
    # Local development server. Render runs the app with Gunicorn.
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
