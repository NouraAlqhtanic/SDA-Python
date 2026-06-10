const form = document.getElementById("resume-form");
const results = document.getElementById("results");

form.addEventListener("submit", function (event) {
  event.preventDefault();

  const jobDescription =
    document.getElementById("job-description").value.trim();

  const customPrompt =
    document.getElementById("custom-prompt").value.trim();

  const fileInput = document.getElementById("resume");

  console.log("Job Description:", jobDescription);
  console.log("Custom Prompt:", customPrompt);

  if (jobDescription === "") {
    results.textContent = "Please enter a job description.";
    return;
  }

  if (fileInput.files.length === 0) {
    results.textContent = "Please upload a PDF resume.";
    return;
  }

  const fileName = fileInput.files[0].name;

  results.textContent =
    `Evaluating ${fileName} against the job description... ` +
    `(ChatGPT integration coming in Stage 5)`;
});