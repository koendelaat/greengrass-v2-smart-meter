if [ $# -ne 2 ]; then
  echo 1>&2 "Usage: $0 COMPONENT_NAME COMPONENT_VERSION"
  exit 3
fi

COMPONENT_NAME=$1
COMPONENT_VERSION=$2
(
cd components/artifacts/$COMPONENT_NAME/$COMPONENT_VERSION/docker || exit

docker run --rm --privileged multiarch/qemu-user-static --reset -p yes
for SUBDIR in *;
do docker buildx build -t koendelaat/${SUBDIR}:$COMPONENT_VERSION --platform linux/amd64,linux/arm/v7 --push ${SUBDIR};
 done
)