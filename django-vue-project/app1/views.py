from django.views import View
from django.http import JsonResponse
from app1.models import Todo
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
class TodoListView(View):
    def get(self, request):
        todos = {
            pk: {"pk": pk, "todo": todo, "is_done": is_done}
            for pk, todo, is_done in Todo.objects.values_list(
                "id",
                "todo",
                "is_done",
            )
        }
        return JsonResponse(todos, safe=False)


@method_decorator(csrf_exempt, name="dispatch")
class TodoCreateView(View):
    def post(self, request):
        print(request.POST.keys())
        data = {"todo": request.POST.get("todo"), "is_done": False}
        todo = Todo(**data)
        todo.save()
        return JsonResponse({"status": "saved", "id": todo.id})


@method_decorator(csrf_exempt, name="dispatch")
class TodoUpdateView(View):
    def put(self, request, pk):
        todo = Todo.objects.get(pk=pk)

        # Workaround
        # https://dzone.com/articles/parsing-unsupported-requests-put-delete-etc-in-dja
        request.method = "POST"
        request._load_post_and_files()
        request.PUT = request.POST
        # End Workaround

        todo.todo = request.PUT.get("todo")
        todo.save()
        return JsonResponse({"status": "saved", "id": todo.id})


@method_decorator(csrf_exempt, name="dispatch")
class TodoDeleteView(View):
    def dispatch(self, request, *args, **kwargs):
        # https://micropyramid.com/blog/introduction-to-django-class-based-views/
        pk = kwargs.get("pk")
        return self.delete(request, pk)

    def delete(self, request, pk):

        # Workaround
        # https://dzone.com/articles/parsing-unsupported-requests-put-delete-etc-in-dja
        request.method = "POST"
        request._load_post_and_files()
        request.DELETE = request.POST
        # End Workaround

        todo_qs = Todo.objects.filter(pk=pk)
        is_todo_exists = todo_qs.exists()
        if is_todo_exists:
            todo = todo_qs.delete()
            return JsonResponse(
                {"status": "deleted"}
            )
        else:
            return JsonResponse({"status": "failed", "message": "deletion failed"})
