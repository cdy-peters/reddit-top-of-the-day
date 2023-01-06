var originalBody;

const inputBody = () => {
  const body = $("#bodyText");
  const saveBtn = $("#saveBodyBtn");

  // Disable save button if body is unchanged
  saveBtn.attr("disabled", body.text() === originalBody);
};

const editBody = () => {
  const body = $("#bodyText");
  const editBtn = $("#editBodyBtn");
  const saveBtn = $("#saveBodyBtn");

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
  const editBtn = $("#editBodyBtn");
  const saveBtn = $("#saveBodyBtn");

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

// Comment
var originalComment;

const inputComment = (commentId) => {
  const comment = $(`#${commentId} #commentText`);
  const saveBtn = $(`#${commentId} #saveBtn`);

  // Disable save button if comment is unchanged
  saveBtn.attr("disabled", comment.text() === originalComment);
};

const editComment = (commentId) => {
  const comment = $(`#${commentId} #commentText`);
  const editBtn = $(`#${commentId} #editBtn`);
  const saveBtn = $(`#${commentId} #saveBtn`);

  if (editBtn.text() === "Edit") {
    originalComment = comment.text();

    comment.attr("contenteditable", true);
    comment.focus();

    saveBtn.attr("hidden", false);
    saveBtn.attr("disabled", true);
    editBtn.text("Cancel");
  } else {
    comment.text(originalComment);
    comment.attr("contenteditable", false);

    saveBtn.attr("hidden", true);
    saveBtn.attr("disabled", true);
    editBtn.text("Edit");
  }
};

const saveComment = (subreddit, id, commentId) => {
  const comment = $(`#${commentId} #commentText`);
  const editBtn = $(`#${commentId} #editBtn`);
  const saveBtn = $(`#${commentId} #saveBtn`);

  $.ajax({
    url: `/edit/comment/${subreddit}/${id}/${commentId}`,
    type: "POST",
    data: {
      comment: comment.text(),
    },
    success: (data) => {
      comment.attr("contenteditable", false);

      saveBtn.attr("hidden", true);
      saveBtn.attr("disabled", true);
      editBtn.text("Edit");
    },
  });
};
