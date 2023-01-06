const remakeBtn = $("#remakeBtn");

// Edit body
var originalBody;

const inputBody = () => {
  const body = $("#bodyText");
  const confirmBtn = $("#confirmBodyBtn");

  // Disable confirm button if body is unchanged
  confirmBtn.attr("disabled", body.text() === originalBody);
};

const editBody = () => {
  const body = $("#bodyText");
  const editBtn = $("#editBodyBtn");
  const confirmBtn = $("#confirmBodyBtn");

  if (editBtn.text() === "Edit") {
    originalBody = body.text();

    body.attr("contenteditable", true);
    body.focus();

    confirmBtn.attr("hidden", false);
    editBtn.text("Cancel");
  } else {
    body.text(originalBody);
    body.attr("contenteditable", false);

    confirmBtn.attr("hidden", true);
    confirmBtn.attr("disabled", true);
    editBtn.text("Edit");
  }
};

const confirmBody = (subreddit, id) => {
  const body = $("#bodyText");
  const editBtn = $("#editBodyBtn");
  const confirmBtn = $("#confirmBodyBtn");

  $.ajax({
    url: `/edit/body/${subreddit}/${id}`,
    type: "POST",
    data: {
      body: body.text(),
    },
    success: (data) => {
      body.attr("contenteditable", false);

      confirmBtn.attr("hidden", true);
      confirmBtn.attr("disabled", true);
      editBtn.text("Edit");

      remakeBtn.attr("hidden", false);
    },
  });
};

// Edit comment
var originalComment;

const inputComment = (commentId) => {
  const comment = $(`#${commentId} #commentText`);
  const confirmBtn = $(`#${commentId} #confirmBtn`);

  // Disable confirm button if comment is unchanged
  confirmBtn.attr("disabled", comment.text() === originalComment);
};

const editComment = (commentId) => {
  const comment = $(`#${commentId} #commentText`);
  const editBtn = $(`#${commentId} #editBtn`);
  const confirmBtn = $(`#${commentId} #confirmBtn`);

  if (editBtn.text() === "Edit") {
    originalComment = comment.text();

    comment.attr("contenteditable", true);
    comment.focus();

    confirmBtn.attr("hidden", false);
    confirmBtn.attr("disabled", true);
    editBtn.text("Cancel");
  } else {
    comment.text(originalComment);
    comment.attr("contenteditable", false);

    confirmBtn.attr("hidden", true);
    confirmBtn.attr("disabled", true);
    editBtn.text("Edit");
  }
};

const confirmComment = (subreddit, id, commentId) => {
  const comment = $(`#${commentId} #commentText`);
  const editBtn = $(`#${commentId} #editBtn`);
  const confirmBtn = $(`#${commentId} #confirmBtn`);

  $.ajax({
    url: `/edit/comment/${subreddit}/${id}/${commentId}`,
    type: "POST",
    data: {
      comment: comment.text(),
    },
    success: (data) => {
      comment.attr("contenteditable", false);

      confirmBtn.attr("hidden", true);
      confirmBtn.attr("disabled", true);
      editBtn.text("Edit");

      remakeBtn.attr("hidden", false);
    },
  });
};
