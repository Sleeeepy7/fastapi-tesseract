from fastapi import APIRouter, Depends

from auth.permissions import PermissionsDependency, IsAuthenticatedPermission


subscription_router = APIRouter()


# @subscription_router.get(
#     "",
#     dependencies=[
#         Depends(
#             PermissionsDependency(
#                 [
#                     IsAuthenticatedPermission,
#                 ]
#             )
#         ),
#     ],
# )
# async def test():
#     return {"test"}


@subscription_router.get(
    "",
)
async def test():
    return {"test"}
