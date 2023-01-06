const remakeBtn = $("#remakeBtn");

const originalThread = { comments: {} };
const editedThread = { comments: {} };

const remakeBtnVisibility = () => {
  !("body" in editedThread) && Object.keys(editedThread.comments).length === 0
    ? remakeBtn.attr("disabled", true)
    : remakeBtn.attr("disabled", false);
};

// Edit body
const body = $("#bodyText");
const editBodyBtn = $("#editBodyBtn");
const confirmBodyBtn = $("#confirmBodyBtn");

const inputBody = () => {
  // Disable confirm button if body is unchanged
  confirmBodyBtn.attr("disabled", body.text() === editedThread.body);
};

const editBody = () => {
  if (editBodyBtn.text() === "Edit") {
    // Add body to originalThread if it doesn't exist
    if (!("body" in originalThread)) originalThread["body"] = body.text();

    body.attr("contenteditable", true);
    body.focus();

    confirmBodyBtn.attr("hidden", false);
    editBodyBtn.text("Cancel");
  } else {
    // Resets body
    body.text(editedThread.body || originalThread.body);

    body.attr("contenteditable", false);

    confirmBodyBtn.attr("hidden", true);
    confirmBodyBtn.attr("disabled", true);
    editBodyBtn.text("Edit");
  }
};

const confirmBody = () => {
  // Check if changed body is the same as the original
  body.text() === originalThread.body
    ? delete editedThread.body
    : (editedThread.body = body.text());

  body.attr("contenteditable", false);

  confirmBodyBtn.attr("hidden", true);
  confirmBodyBtn.attr("disabled", true);
  editBodyBtn.text("Edit");

  remakeBtnVisibility();
};

// Edit comment
const inputComment = (commentId) => {
  const comment = $(`#${commentId} #commentText`);
  const confirmBtn = $(`#${commentId} #confirmBtn`);

  // Disable confirm button if comment is unchanged
  var bool;

  editedThread.comments[commentId]
    ? (bool = editedThread.comments[commentId])
    : (bool = originalThread.comments[commentId]);

  confirmBtn.attr("disabled", comment.text() === bool);
};

const editComment = (commentId) => {
  const comment = $(`#${commentId} #commentText`);
  const editBtn = $(`#${commentId} #editBtn`);
  const confirmBtn = $(`#${commentId} #confirmBtn`);

  if (editBtn.text() === "Edit") {
    // Add comment to originalThread if it doesn't exist
    if (!(commentId in originalThread.comments))
      originalThread.comments[commentId] = comment.text();

    comment.attr("contenteditable", true);
    comment.focus();

    confirmBtn.attr("hidden", false);
    editBtn.text("Cancel");
  } else {
    // Resets comment
    commentId in editedThread.comments
      ? comment.text(editedThread.comments[commentId])
      : comment.text(originalThread.comments[commentId]);

    comment.attr("contenteditable", false);

    confirmBtn.attr("hidden", true);
    confirmBtn.attr("disabled", true);
    editBtn.text("Edit");
  }
};

const confirmComment = (commentId) => {
  const comment = $(`#${commentId} #commentText`);
  const editBtn = $(`#${commentId} #editBtn`);
  const confirmBtn = $(`#${commentId} #confirmBtn`);

  // Check if changed comment is the same as the original
  comment.text() === originalThread.comments[commentId]
    ? delete editedThread.comments[commentId]
    : (editedThread.comments[commentId] = comment.text());

  comment.attr("contenteditable", false);

  confirmBtn.attr("hidden", true);
  confirmBtn.attr("disabled", true);
  editBtn.text("Edit");

  remakeBtnVisibility();
};

const queueRemake = (subreddit, thread) => {
  $.ajax({
    url: `/queue_remake/${subreddit}/${thread}`,
    type: "POST",
    dataType: "json",
    data: JSON.stringify(editedThread),
    contentType: "application/json",
    success: () => {
      window.location.href = "/";
    },
  });
};
