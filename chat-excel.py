import os, sys, time, pandas, openai

openai.api_key = os.getenv("OPENAI_API_KEY")


def get_response(prompt):
    for _ in range(5):
        try:
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=prompt,
                temperature=0,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0,
                max_tokens=64,
            )
            return response["choices"][0]["text"].strip()

        except openai.error.RateLimitError:
            print("Reached rate limit, sleeping for 60 seconds.")
            time.sleep(60)
    raise Exception("Timeout Error")


file_name = sys.argv[1]
out_file = file_name.replace(".xlsx", ".csv")
df = pandas.read_excel(file_name)

with open(out_file, "w") as f:
    for row in df.values:
        prompt = f"{row[1]}{row[2]}?"
        response = get_response(prompt)
        f.write(f'"{row[1]}{row[2]}","{response}"\n')
