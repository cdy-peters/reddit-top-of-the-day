var originalBody;

const inputBody = () => {
  const body = $("#bodyText");
  const saveBtn = $("#saveBtn");

  // Disable save button if body is unchanged
  saveBtn.attr("disabled", body.text() === originalBody);
};

const editBody = () => {
  const body = $("#bodyText");
  const editBtn = $("#editBtn");
  const saveBtn = $("#saveBtn");

  if (editBtn.text() === "Edit") {
    originalBody = body.text();

    body.attr("contenteditable", true);
    body.focus();

    saveBtn.attr("hidden", false);
    editBtn.text("Cancel");
  } else {
    body.text(originalBody);
    body.attr("contenteditable", false);

    saveBtn.attr("hidden", true);
    saveBtn.attr("disabled", true);
    editBtn.text("Edit");
  }
};

const saveBody = (subreddit, id) => {
  const body = $("#bodyText");
  const editBtn = $("#editBtn");
  const saveBtn = $("#saveBtn");

  $.ajax({
    url: `/edit/body/${subreddit}/${id}`,
    type: "POST",
    data: {
      body: body.text(),
    },
    success: (data) => {
      body.attr("contenteditable", false);

      saveBtn.attr("hidden", true);
      saveBtn.attr("disabled", true);
      editBtn.text("Edit");
    },
  });
};
